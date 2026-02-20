import numpy as np
import yaml
from pathlib import Path
import dill


from exceptions import CustomException
from logging_core import LoggerFactory
from typing import Union, List
import pickle

logger = LoggerFactory.get_logger(__name__,level="DEBUG")


def read_yaml(file_path: str) -> dict:
    try:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"YAML file not found at {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        if content is None:
            raise ValueError("YAML file is empty")

        logger.info(f"YAML file loaded successfully: {file_path}")

        return content

    except Exception as e:
        logger.error("Failed to read YAML file", exc_info=True)
        raise CustomException(
            message="Error while reading YAML file",
            original_exception=e
        )


def write_yaml(file_path: str, data: dict, create_dir: bool = True) -> None:
    """
    Writes dictionary data to a YAML file.

    Parameters
    ----------
    file_path : str
        Path where YAML file should be written
    data : dict
        Data to write
    create_dir : bool
        Automatically create directory if not exists
    """
    try:
        path = Path(file_path)

        # Creating parent directory if needed
        if create_dir:
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                data,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )

        logger.info(f"YAML file written successfully at: {file_path}")

    except Exception as e:
        logger.error("Failed to write YAML file", exc_info=True)
        raise CustomException(
            message="Error while writing YAML file",
            original_exception=e,
        )

def load_object(file_path: str) -> object:
    try:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Object file not found at {file_path}")

        # Trying pickle first
        try:
            with open(path, "rb") as f:
                obj = pickle.load(f)
            logger.info("Object loaded using pickle")
            return obj


        except Exception as pickle_error:
            logger.warning(f"Pickle load failed: {pickle_error}")
            logger.warning("Pickle load failed, trying dill")

            with open(path, "rb") as f:
                obj = dill.load(f)

            logger.info("Object loaded using dill")
            return obj

    except Exception as e:
        logger.error("Failed to load object", exc_info=True)
        raise CustomException(
            message="Error while loading object",
            original_exception=e
        )



def save_object(file_path: str, obj: object, create_dir: bool = True) -> None:
    try:
        path = Path(file_path)

        if create_dir:
            path.parent.mkdir(parents=True, exist_ok=True)

        # Try pickle first (faster)
        try:
            with open(path, "wb") as f:
                pickle.dump(obj, f)
            logger.info("Object saved using pickle")

        except Exception:
            logger.warning("Pickle failed, falling back to dill")

            with open(path, "wb") as f:
                dill.dump(obj, f)

            logger.info("Object saved using dill")

    except Exception as e:
        logger.error("Failed to save object", exc_info=True)
        raise CustomException(
            message="Error while saving object",
            original_exception=e
        )

def save_numpy_array_data(file_path: str, array: np.ndarray, create_dir: bool = True) -> None:
    """
    Saves a NumPy array to a .npy file.

    Parameters
    ----------
    file_path : str
        Path where array should be saved
    array : np.ndarray
        Numpy array to save
    create_dir : bool
        Whether to create parent directories automatically
    """
    try:
        path = Path(file_path)

        if create_dir:
            path.parent.mkdir(parents=True, exist_ok=True)

        if not isinstance(array, np.ndarray):
            raise TypeError("Input must be a numpy.ndarray")

        np.save(path, array)

        logger.info(f"Numpy array saved successfully at: {file_path}")

    except Exception as e:
        logger.error("Failed to save numpy array", exc_info=True)
        raise CustomException(
            message="Error while saving numpy array",
            original_exception=e
        )

def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    Loads a NumPy array from a .npy file.
    """
    try:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Numpy file not found at {file_path}")

        array = np.load(path)

        logger.info(f"Numpy array loaded successfully from: {file_path}")

        return array

    except Exception as e:
        logger.error("Failed to load numpy array", exc_info=True)
        raise CustomException(
            message="Error while loading numpy array",
            original_exception=e
        )


def create_directories(
    paths: Union[str, List[str]],
    exist_ok: bool = True
) -> None:
    """
    Creates one or multiple directories.

    Parameters
    ----------
    paths : str | List[str]
        Single path or list of directory paths
    exist_ok : bool
        If True, ignores error if directory already exists
    """
    try:
        # Convert single string to list
        if isinstance(paths, str):
            paths = [paths]

        for path in paths:
            Path(path).mkdir(parents=True, exist_ok=exist_ok)
            logger.info(f"Directory created or already exists: {path}")

    except Exception as e:
        logger.error("Failed to create directories", exc_info=True)
        raise CustomException(
            message="Error while creating directories",
            original_exception=e
        )