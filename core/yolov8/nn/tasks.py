import contextlib
from copy import deepcopy
from pathlib import Path

import torch
import torch.nn as nn

try:
    import thop
except ImportError:
    thop = None

from core.yolov8.nn.modules import *
from core.yolov8.yolov8_utils import DEFAULT_CFG_DICT, yaml_load
from core.yolov8.yolov8_utils.checks import check_suffix, check_yaml
from core.yolov8.yolov8_utils.loss import E2EDetectLoss, v8DetectionLoss
from core.yolov8.yolov8_utils.torch_utils import initialize_weights, make_divisible, scale_img


class BaseModel(nn.Module):
    """The BaseModel class serves as a base class for all the models in the Ultralytics YOLO family."""

    def forward(self, x, *args, **kwargs):
        """
        Forward pass of the model on a single scale. Wrapper for `_forward_once` method.

        Args:
            x (torch.Tensor | dict): The input image tensor or a dict including image tensor and gt labels.

        Returns:
            (torch.Tensor): The output of the network.
        """
        if isinstance(x, dict):  # for cases of training and validating while training.
            return self.loss(x, *args, **kwargs)
        return self.predict(x, *args, **kwargs)

    def predict(self, x, profile=False, visualize=False, augment=False, embed=None):
        """
        Perform a forward pass through the network.

        Args:
            x (torch.Tensor): The input tensor to the model.
            profile (bool):  Print the computation time of each layer if True, defaults to False.
            visualize (bool): Save the feature maps of the model if True, defaults to False.
            augment (bool): Augment image during prediction, defaults to False.
            embed (list, optional): A list of feature vectors/embeddings to return.

        Returns:
            (torch.Tensor): The last output of the model.
        """
        if augment:
            return self._predict_augment(x)
        return self._predict_once(x, profile, visualize, embed)

    def _predict_once(self, x, profile=False, visualize=False, embed=None):
        """
        Perform a forward pass through the network.

        Args:
            x (torch.Tensor): The input tensor to the model.
            profile (bool):  Print the computation time of each layer if True, defaults to False.
            visualize (bool): Save the feature maps of the model if True, defaults to False.
            embed (list, optional): A list of feature vectors/embeddings to return.

        Returns:
            (torch.Tensor): The last output of the model.
        """
        y, dt, embeddings = [], [], []  # outputs
        for m in self.model:
            if m.f != -1:  # if not from previous layer
                x = y[m.f] if isinstance(m.f, int) else [x if j == -1 else y[j] for j in m.f]  # from earlier layers
            if profile:
                self._profile_one_layer(m, x, dt)
            x = m(x)  # run
            y.append(x if m.i in self.save else None)  # save output
            # if visualize:
            #     feature_visualization(x, m.type, m.i, save_dir=visualize)
            if embed and m.i in embed:
                embeddings.append(nn.functional.adaptive_avg_pool2d(x, (1, 1)).squeeze(-1).squeeze(-1))  # flatten
                if m.i == max(embed):
                    return torch.unbind(torch.cat(embeddings, 1), dim=0)
        return x

    # def _predict_augment(self, x):
    #     """Perform augmentations on input image x and return augmented inference."""
    #     print(
    #         f"WARNING ⚠️ {self.__class__.__name__} does not support 'augment=True' prediction. "
    #         f"Reverting to single-scale prediction."
    #     )
    #     return self._predict_once(x)
    #
    # def _profile_one_layer(self, m, x, dt):
    #     """
    #     Profile the computation time and FLOPs of a single layer of the model on a given input. Appends the results to
    #     the provided list.
    #
    #     Args:
    #         m (nn.Module): The layer to be profiled.
    #         x (torch.Tensor): The input data to the layer.
    #         dt (list): A list to store the computation time of the layer.
    #
    #     Returns:
    #         None
    #     """
    #     c = m == self.model[-1] and isinstance(x, list)  # is final layer list, copy input as inplace fix
    #     flops = thop.profile(m, inputs=[x.copy() if c else x], verbose=False)[0] / 1e9 * 2 if thop else 0  # GFLOPs
    #     t = time_sync()
    #     for _ in range(10):
    #         m(x.copy() if c else x)
    #     dt.append((time_sync() - t) * 100)
    #     if m == self.model[0]:
    #         print(f"{'time (ms)':>10s} {'GFLOPs':>10s} {'params':>10s}  module")
    #     print(f"{dt[-1]:10.2f} {flops:10.2f} {m.np:10.0f}  {m.type}")
    #     if c:
    #         print(f"{sum(dt):10.2f} {'-':>10s} {'-':>10s}  Total")
    #
    # def fuse(self, verbose=True):
    #     """
    #     Fuse the `Conv2d()` and `BatchNorm2d()` layers of the model into a single layer, in order to improve the
    #     computation efficiency.
    #
    #     Returns:
    #         (nn.Module): The fused model is returned.
    #     """
    #     if not self.is_fused():
    #         for m in self.model.modules():
    #             if isinstance(m, (Conv, Conv2, DWConv)) and hasattr(m, "bn"):
    #                 if isinstance(m, Conv2):
    #                     m.fuse_convs()
    #                 m.conv = fuse_conv_and_bn(m.conv, m.bn)  # update conv
    #                 delattr(m, "bn")  # remove batchnorm
    #                 m.forward = m.forward_fuse  # update forward
    #             if isinstance(m, ConvTranspose) and hasattr(m, "bn"):
    #                 m.conv_transpose = fuse_deconv_and_bn(m.conv_transpose, m.bn)
    #                 delattr(m, "bn")  # remove batchnorm
    #                 m.forward = m.forward_fuse  # update forward
    #             if isinstance(m, RepConv):
    #                 m.fuse_convs()
    #                 m.forward = m.forward_fuse  # update forward
    #             if isinstance(m, RepVGGDW):
    #                 m.fuse()
    #                 m.forward = m.forward_fuse
    #         self.info(verbose=verbose)
    #
    #     return self
    #
    # def is_fused(self, thresh=10):
    #     """
    #     Check if the model has less than a certain threshold of BatchNorm layers.
    #
    #     Args:
    #         thresh (int, optional): The threshold number of BatchNorm layers. Default is 10.
    #
    #     Returns:
    #         (bool): True if the number of BatchNorm layers in the model is less than the threshold, False otherwise.
    #     """
    #     bn = tuple(v for k, v in nn.__dict__.items() if "Norm" in k)  # normalization layers, i.e. BatchNorm2d()
    #     return sum(isinstance(v, bn) for v in self.modules()) < thresh  # True if < 'thresh' BatchNorm layers in model
    #
    # def info(self, detailed=False, verbose=True, imgsz=640):
    #     """
    #     Prints model information.
    #
    #     Args:
    #         detailed (bool): if True, prints out detailed information about the model. Defaults to False
    #         verbose (bool): if True, prints out the model information. Defaults to False
    #         imgsz (int): the size of the image that the model will be trained on. Defaults to 640
    #     """
    #     return model_info(self, detailed=detailed, verbose=verbose, imgsz=imgsz)
    #
    # def _apply(self, fn):
    #     """
    #     Applies a function to all the tensors in the model that are not parameters or registered buffers.
    #
    #     Args:
    #         fn (function): the function to apply to the model
    #
    #     Returns:
    #         (BaseModel): An updated BaseModel object.
    #     """
    #     self = super()._apply(fn)
    #     m = self.model[-1]  # Detect()
    #     if isinstance(m, Detect):  # includes all Detect subclasses like Segment, Pose, OBB, WorldDetect
    #         m.stride = fn(m.stride)
    #         m.anchors = fn(m.anchors)
    #         m.strides = fn(m.strides)
    #     return self
    #
    # def load(self, weights, verbose=True):
    #     """
    #     Load the weights into the model.
    #
    #     Args:
    #         weights (dict | torch.nn.Module): The pre-trained weights to be loaded.
    #         verbose (bool, optional): Whether to log the transfer progress. Defaults to True.
    #     """
    #     model = weights["model"] if isinstance(weights, dict) else weights  # torchvision models are not dicts
    #     csd = model.float().state_dict()  # checkpoint state_dict as FP32
    #     csd = intersect_dicts(csd, self.state_dict())  # intersect
    #     self.load_state_dict(csd, strict=False)  # load
    #     if verbose:
    #         LOGGER.info(f"Transferred {len(csd)}/{len(self.model.state_dict())} items from pretrained weights")
    #
    # def loss(self, batch, preds=None):
    #     """
    #     Compute loss.
    #
    #     Args:
    #         batch (dict): Batch to compute loss on
    #         preds (torch.Tensor | List[torch.Tensor]): Predictions.
    #     """
    #     if getattr(self, "criterion", None) is None:
    #         self.criterion = self.init_criterion()
    #
    #     preds = self.forward(batch["img"]) if preds is None else preds
    #     return self.criterion(preds, batch)
    #
    # def init_criterion(self):
    #     """Initialize the loss criterion for the BaseModel."""
    #     raise NotImplementedError("compute_loss() needs to be implemented by task heads")


class DetectionModel(BaseModel):
    """YOLOv8 detection model."""

    def __init__(self, cfg="yolov8n.yaml", ch=3, nc=None, verbose=True):  # model, input channels, number of classes
        """Initialize the YOLOv8 detection model with the given config and parameters."""
        super().__init__()
        self.yaml = cfg if isinstance(cfg, dict) else yaml_model_load(cfg)  # cfg dict
        if self.yaml["backbone"][0][2] == "Silence":
            print(
                "WARNING ⚠️ YOLOv9 `Silence` module is deprecated in favor of nn.Identity. "
                "Please delete local *.pt file and re-download the latest model checkpoint."
            )
            self.yaml["backbone"][0][2] = "nn.Identity"

        # Define model
        ch = self.yaml["ch"] = self.yaml.get("ch", ch)  # input channels
        if nc and nc != self.yaml["nc"]:
            print(f"Overriding model.yaml nc={self.yaml['nc']} with nc={nc}")
            self.yaml["nc"] = nc  # override YAML value
        self.model, self.save = parse_model(deepcopy(self.yaml), ch=ch, verbose=verbose)  # model, savelist
        self.names = {i: f"{i}" for i in range(self.yaml["nc"])}  # default names dict
        self.inplace = self.yaml.get("inplace", True)
        self.end2end = getattr(self.model[-1], "end2end", False)

        # Build strides
        m = self.model[-1]  # Detect()
        if isinstance(m, Detect):  # includes all Detect subclasses like Segment, Pose, OBB, WorldDetect
            s = 256  # 2x min stride
            m.inplace = self.inplace

            def _forward(x):
                """Performs a forward pass through the model, handling different Detect subclass types accordingly."""
                if self.end2end:
                    return self.forward(x)["one2many"]
                return self.forward(x)[0] if isinstance(m, (Segment, Pose, OBB)) else self.forward(x)

            m.stride = torch.tensor([s / x.shape[-2] for x in _forward(torch.zeros(1, ch, s, s))])  # forward
            self.stride = m.stride
            m.bias_init()  # only run once
        else:
            self.stride = torch.Tensor([32])  # default stride for i.e. RTDETR

        # Init weights, biases
        initialize_weights(self)
        if verbose:
            self.info()
            print("")

    def _predict_augment(self, x):
        """Perform augmentations on input image x and return augmented inference and train outputs."""
        if getattr(self, "end2end", False):
            print(
                "WARNING ⚠️ End2End model does not support 'augment=True' prediction. "
                "Reverting to single-scale prediction."
            )
            return self._predict_once(x)
        img_size = x.shape[-2:]  # height, width
        s = [1, 0.83, 0.67]  # scales
        f = [None, 3, None]  # flips (2-ud, 3-lr)
        y = []  # outputs
        for si, fi in zip(s, f):
            xi = scale_img(x.flip(fi) if fi else x, si, gs=int(self.stride.max()))
            yi = super().predict(xi)[0]  # forward
            yi = self._descale_pred(yi, fi, si, img_size)
            y.append(yi)
        y = self._clip_augmented(y)  # clip augmented tails
        return torch.cat(y, -1), None  # augmented inference, train

    @staticmethod
    def _descale_pred(p, flips, scale, img_size, dim=1):
        """De-scale predictions following augmented inference (inverse operation)."""
        p[:, :4] /= scale  # de-scale
        x, y, wh, cls = p.split((1, 1, 2, p.shape[dim] - 4), dim)
        if flips == 2:
            y = img_size[0] - y  # de-flip ud
        elif flips == 3:
            x = img_size[1] - x  # de-flip lr
        return torch.cat((x, y, wh, cls), dim)

    def _clip_augmented(self, y):
        """Clip YOLO augmented inference tails."""
        nl = self.model[-1].nl  # number of detection layers (P3-P5)
        g = sum(4**x for x in range(nl))  # grid points
        e = 1  # exclude layer count
        i = (y[0].shape[-1] // g) * sum(4**x for x in range(e))  # indices
        y[0] = y[0][..., :-i]  # large
        i = (y[-1].shape[-1] // g) * sum(4 ** (nl - 1 - x) for x in range(e))  # indices
        y[-1] = y[-1][..., i:]  # small
        return y

    def init_criterion(self):
        """Initialize the loss criterion for the DetectionModel."""
        return E2EDetectLoss(self) if getattr(self, "end2end", False) else v8DetectionLoss(self)


class Ensemble(nn.ModuleList):
    """Ensemble of models."""

    def __init__(self):
        """Initialize an ensemble of models."""
        super().__init__()

    def forward(self, x, augment=False, profile=False, visualize=False):
        """Function generates the YOLO network's final layer."""
        y = [module(x, augment, profile, visualize)[0] for module in self]
        # y = torch.stack(y).max(0)[0]  # max ensemble
        # y = torch.stack(y).mean(0)  # mean ensemble
        y = torch.cat(y, 2)  # nms ensemble, y shape(B, HW, C)
        return y, None  # inference, train output


@contextlib.contextmanager
def temporary_modules(modules=None):
    """
    Context manager for temporarily adding or modifying modules in Python's module cache (`sys.modules`).

    This function can be used to change the module paths during runtime. It's useful when refactoring code,
    where you've moved a module from one location to another, but you still want to support the old import
    paths for backwards compatibility.

    Args:
        modules (dict, optional): A dictionary mapping old module paths to new module paths.

    Example:
        ```python
        with temporary_modules({'old.module.path': 'new.module.path'}):
            import old.module.path  # this will now import new.module.path
        ```

    Note:
        The changes are only in effect inside the context manager and are undone once the context manager exits.
        Be aware that directly manipulating `sys.modules` can lead to unpredictable results, especially in larger
        applications or libraries. Use this function with caution.
    """
    if not modules:
        modules = {}

    import importlib
    import sys

    try:
        # Set modules in sys.modules under their old name
        for old, new in modules.items():
            sys.modules[old] = importlib.import_module(new)

        yield
    finally:
        # Remove the temporary module paths
        for old in modules:
            if old in sys.modules:
                del sys.modules[old]


def torch_safe_load(weight):
    from core.yolov8.yolov8_utils.downloads import attempt_download_asset
    check_suffix(file=weight, suffix=".pt")
    file = attempt_download_asset(weight)  # search online if missing locally
    try:
        with temporary_modules(
            {
                "ultralytics": "core.yolov8"
            }
        ):
            ckpt = torch.load(file, map_location="cpu")
    except ModuleNotFoundError as e:
        print(e)
    return ckpt, file  # load


def attempt_load_weights(weights, device=None, inplace=True, fuse=False):
    """Loads an ensemble of models weights=[a,b,c] or a single model weights=[a] or weights=a."""

    ensemble = Ensemble()
    for w in weights if isinstance(weights, list) else [weights]:
        ckpt, w = torch_safe_load(w)  # load ckpt
        args = {**DEFAULT_CFG_DICT, **ckpt["train_args"]} if "train_args" in ckpt else None  # combined args
        model = (ckpt.get("ema") or ckpt["model"]).to(device).float()  # FP32 model

        # Model compatibility updates
        model.args = args  # attach args to model
        model.pt_path = w  # attach *.pt file path to model
        model.task = guess_model_task(model)
        if not hasattr(model, "stride"):
            model.stride = torch.tensor([32.0])

        # Append
        ensemble.append(model.fuse().eval() if fuse and hasattr(model, "fuse") else model.eval())  # model in eval mode

    # Module updates
    for m in ensemble.modules():
        t = type(m)
        if t in (nn.Hardswish, nn.LeakyReLU, nn.ReLU, nn.ReLU6, nn.SiLU, Detect):  #, OBB):
            m.inplace = inplace
        elif t is nn.Upsample and not hasattr(m, "recompute_scale_factor"):
            m.recompute_scale_factor = None  # torch 1.11.0 compatibility

    # Return model
    if len(ensemble) == 1:
        return ensemble[-1]

    # Return ensemble
    print(f"Ensemble created with {weights}\n")
    for k in "names", "nc", "yaml":
        setattr(ensemble, k, getattr(ensemble[0], k))
    ensemble.stride = ensemble[torch.argmax(torch.tensor([m.stride.max() for m in ensemble])).int()].stride
    assert all(ensemble[0].nc == m.nc for m in ensemble), f"Models differ in class counts {[m.nc for m in ensemble]}"
    return ensemble


def parse_model(d, ch, verbose=True):  # model_dict, input_channels(3)
    """Parse a YOLO model.yaml dictionary into a PyTorch model."""
    import ast

    # Args
    max_channels = float("inf")
    nc, act, scales = (d.get(x) for x in ("nc", "activation", "scales"))
    depth, width, kpt_shape = (d.get(x, 1.0) for x in ("depth_multiple", "width_multiple", "kpt_shape"))
    if scales:
        scale = d.get("scale")
        if not scale:
            scale = tuple(scales.keys())[0]
            print(f"WARNING ⚠️ no model scale passed. Assuming scale='{scale}'.")
        depth, width, max_channels = scales[scale]

    if act:
        Conv.default_act = eval(act)  # redefine default activation, i.e. Conv.default_act = nn.SiLU()
        if verbose:
            print(f"{'activation:'} {act}")  # print

    if verbose:
        print(f"\n{'':>3}{'from':>20}{'n':>3}{'params':>10}  {'module':<45}{'arguments':<30}")
    ch = [ch]
    layers, save, c2 = [], [], ch[-1]  # layers, savelist, ch out
    for i, (f, n, m, args) in enumerate(d["backbone"] + d["head"]):  # from, number, module, args
        m = getattr(torch.nn, m[3:]) if "nn." in m else globals()[m]  # get module
        for j, a in enumerate(args):
            if isinstance(a, str):
                with contextlib.suppress(ValueError):
                    args[j] = locals()[a] if a in locals() else ast.literal_eval(a)

        n = n_ = max(round(n * depth), 1) if n > 1 else n  # depth gain
        if m in {
            Classify,
            Conv,
            ConvTranspose,
            GhostConv,
            Bottleneck,
            GhostBottleneck,
            SPP,
            SPPF,
            DWConv,
            Focus,
            BottleneckCSP,
            C1,
            C2,
            C2f,
            RepNCSPELAN4,
            ELAN1,
            ADown,
            AConv,
            SPPELAN,
            C2fAttn,
            C3,
            C3TR,
            C3Ghost,
            nn.ConvTranspose2d,
            DWConvTranspose2d,
            C3x,
            RepC3,
            PSA,
            SCDown,
            C2fCIB,
        }:
            c1, c2 = ch[f], args[0]
            if c2 != nc:  # if c2 not equal to number of classes (i.e. for Classify() output)
                c2 = make_divisible(min(c2, max_channels) * width, 8)
            if m is C2fAttn:
                args[1] = make_divisible(min(args[1], max_channels // 2) * width, 8)  # embed channels
                args[2] = int(
                    max(round(min(args[2], max_channels // 2 // 32)) * width, 1) if args[2] > 1 else args[2]
                )  # num heads

            args = [c1, c2, *args[1:]]
            if m in {BottleneckCSP, C1, C2, C2f, C2fAttn, C3, C3TR, C3Ghost, C3x, RepC3, C2fCIB}:
                args.insert(2, n)  # number of repeats
                n = 1
        elif m is AIFI:
            args = [ch[f], *args]
        elif m in {HGStem, HGBlock}:
            c1, cm, c2 = ch[f], args[0], args[1]
            args = [c1, cm, c2, *args[2:]]
            if m is HGBlock:
                args.insert(4, n)  # number of repeats
                n = 1
        elif m is ResNetLayer:
            c2 = args[1] if args[3] else args[1] * 4
        elif m is nn.BatchNorm2d:
            args = [ch[f]]
        elif m is Concat:
            c2 = sum(ch[x] for x in f)
        elif m in {Detect, WorldDetect, Segment, Pose, OBB, ImagePoolingAttn, v10Detect}:
            args.append([ch[x] for x in f])
            if m is Segment:
                args[2] = make_divisible(min(args[2], max_channels) * width, 8)
        elif m is RTDETRDecoder:  # special case, channels arg must be passed in index 1
            args.insert(1, [ch[x] for x in f])
        elif m is CBLinear:
            c2 = args[0]
            c1 = ch[f]
            args = [c1, c2, *args[1:]]
        elif m is CBFuse:
            c2 = ch[f[-1]]
        else:
            c2 = ch[f]

        m_ = nn.Sequential(*(m(*args) for _ in range(n))) if n > 1 else m(*args)  # module
        t = str(m)[8:-2].replace("__main__.", "")  # module type
        m.np = sum(x.numel() for x in m_.parameters())  # number params
        m_.i, m_.f, m_.type = i, f, t  # attach index, 'from' index, type
        if verbose:
            print(f"{i:>3}{str(f):>20}{n_:>3}{m.np:10.0f}  {t:<45}{str(args):<30}")  # print
        save.extend(x % i for x in ([f] if isinstance(f, int) else f) if x != -1)  # append to savelist
        layers.append(m_)
        if i == 0:
            ch = []
        ch.append(c2)
    return nn.Sequential(*layers), sorted(save)


def yaml_model_load(path):
    """Load a YOLOv8 model from a YAML file."""
    import re

    path = Path(path)
    if path.stem in (f"yolov{d}{x}6" for x in "nsmlx" for d in (5, 8)):
        new_stem = re.sub(r"(\d+)([nslmx])6(.+)?$", r"\1\2-p6\3", path.stem)
        print(f"WARNING ⚠️ Ultralytics YOLO P6 models now use -p6 suffix. Renaming {path.stem} to {new_stem}.")
        path = path.with_name(new_stem + path.suffix)

    unified_path = re.sub(r"(\d+)([nslmx])(.+)?$", r"\1\3", str(path))  # i.e. yolov8x.yaml -> yolov8.yaml
    yaml_file = check_yaml(unified_path, hard=False) or check_yaml(path)
    d = yaml_load(yaml_file)  # model dict
    d["scale"] = guess_model_scale(path)
    d["yaml_file"] = str(path)
    return d


def guess_model_scale(model_path):
    """
    Takes a path to a YOLO model's YAML file as input and extracts the size character of the model's scale. The function
    uses regular expression matching to find the pattern of the model scale in the YAML file name, which is denoted by
    n, s, m, l, or x. The function returns the size character of the model scale as a string.

    Args:
        model_path (str | Path): The path to the YOLO model's YAML file.

    Returns:
        (str): The size character of the model's scale, which can be n, s, m, l, or x.
    """
    with contextlib.suppress(AttributeError):
        import re

        return re.search(r"yolov\d+([nslmx])", Path(model_path).stem).group(1)  # n, s, m, l, or x
    return ""


def guess_model_task(model):
    """
    Guess the task of a PyTorch model from its architecture or configuration.

    Args:
        model (nn.Module | dict): PyTorch model or model configuration in YAML format.

    Returns:
        (str): Task of the model ('detect', 'segment', 'classify', 'pose').

    Raises:
        SyntaxError: If the task of the model could not be determined.
    """
    def cfg2task(cfg):
        """Guess from YAML dictionary."""
        m = cfg["head"][-1][-2].lower()  # output module name
        if m in ("classify", "classifier", "cls", "fc"):
            return "classify"
        if m == "detect":
            return "detect"
        if m == "segment":
            return "segment"
        if m == "pose":
            return "pose"
        if m == "obb":
            return "obb"

    # Guess from model cfg
    if isinstance(model, dict):
        with contextlib.suppress(Exception):
            return cfg2task(model)

    # Guess from PyTorch model
    if isinstance(model, nn.Module):  # PyTorch model
        for x in "model.args", "model.model.args", "model.model.model.args":
            with contextlib.suppress(Exception):
                return eval(x)["task"]
        for x in "model.yaml", "model.model.yaml", "model.model.model.yaml":
            with contextlib.suppress(Exception):
                return cfg2task(eval(x))

        for m in model.modules():
            if isinstance(m, Detect):
                return "detect"
            # elif isinstance(m, OBB):
            #     return "obb"

    # Guess from model filename
    if isinstance(model, (str, Path)):
        model = Path(model)
        # if "-obb" in model.stem or "obb" in model.parts:
        #     return "obb"
        if "detect" in model.parts:
            return "detect"

    # Unable to determine task from model
    print(
        "WARNING ⚠️ Unable to automatically guess model task, assuming 'task=detect'. "
        "Explicitly define task for your model, i.e. 'task=detect', 'segment', 'classify','pose' or 'obb'."
    )
    return "detect"  # assume detect
