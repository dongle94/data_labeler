import yaml


class Namespace(object):
    pass


config = Namespace()


def set_config(file):
    with open(file, 'r') as f:
        _config = yaml.load(f, Loader=yaml.FullLoader)

    # DB
    config.database = _config['DB']['DATABASE']
    config.host = _config['DB']['HOST']
    config.port = _config['DB']['PORT']
    config.user = _config['DB']['USER']
    config.password = _config['DB']['PASSWORD']

    # WEED
    config.weed_master_url = _config['WEED']['MASTER_URL']
    config.weed_collection_name = _config['WEED']['COLLECTION']
    config.weed_collection_count = _config['WEED']['COLLECTION_COUNT']
    config.weed_use_public_url = _config['WEED']['USE_PUBLIC_URL']

    # Inference
    config.device = _config['ENV']['DEVICE']
    config.gpu_num = _config['ENV']['GPU_NUM']
    # Det
    config.det_model_type = _config['DET']['MODEL_TYPE']
    config.det_model_path = _config['DET']['DET_MODEL_PATH']
    config.det_half = _config['DET']['HALF']
    config.det_conf_thres = _config['DET']['CONF_THRES']
    config.det_obj_classes = eval(str(_config['DET']['OBJ_CLASSES']))
    # YOLO
    config.yolo_img_size = _config['DET']['YOLO']['IMG_SIZE']
    config.yolo_nms_iou = _config['DET']['YOLO']['NMS_IOU']
    config.yolo_agnostic_nms = _config['DET']['YOLO']['AGNOSTIC_NMS']
    config.yolo_max_det = _config['DET']['YOLO']['MAX_DET']
    # INFER
    config.det_infer_cls = _config['DET']['INFER']

    # Logger
    config.log_level = _config['LOG']['LOG_LEVEL']
    config.logger_name = _config['LOG']['LOGGER_NAME']
    config.console_log = _config['LOG']['CONSOLE_LOG']
    config.console_log_interval = _config['LOG']['CONSOLE_LOG_INTERVAL']
    config.file_log = _config['LOG']['FILE_LOG']
    config.file_log_dir = _config['LOG']['FILE_LOG_DIR']
    config.file_log_counter = _config['LOG']['FILE_LOG_COUNTER']
    config.file_log_rotate_time = _config['LOG']['FILE_LOG_ROTATE_TIME']
    config.file_log_rotate_interval = _config['LOG']['FILE_LOG_ROTATE_INTERVAL']


def get_config():
    return config
