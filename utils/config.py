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
    config.user = _config['DB']['USER']
    config.password = _config['DB']['PASSWORD']

    # Env
    # config.device = _config['ENV']['DEVICE']
    # config.gpu_num = _config['ENV']['GPU_NUM']

    # Det
    # config.det_model_type = _config['DET']['MODEL_TYPE']
    # config.det_model_path = _config['DET']['DET_MODEL_PATH']
    # config.det_half = _config['DET']['HALF']
    # config.det_conf_thres = _config['DET']['CONF_THRES']
    # config.det_obj_classes = _config['DET']['OBJ_CLASSES']

    # YOLOV5
    # config.yolov5_img_size = _config['YOLOV5']['IMG_SIZE']
    # config.yolov5_nms_iou = _config['YOLOV5']['NMS_IOU']
    # config.yolov5_agnostic_nms = _config['YOLOV5']['AGNOSTIC_NMS']
    # config.yolov5_max_det = _config['YOLOV5']['MAX_DET']

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
