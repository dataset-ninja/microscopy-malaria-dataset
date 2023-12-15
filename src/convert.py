# https://air.ug/microscopy_dataset/

import glob
import os
import shutil
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "microscopy based diagnostics"
    dataset_path = "/home/grokhi/rawdata/microscopy-dataset"
    batch_size = 30

    images_ext = ".jpg"
    ann_ext = ".xml"

    def create_ann(image_path):
        labels = []
        tags = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        if curr_data == "plasmodium-images":
            ann_path = image_path.replace("/images/", "/annotation/").replace(images_ext, ann_ext)
            child = 5
        else:
            ann_path = image_path.replace(images_ext, ann_ext)
            child = 4

        tree = ET.parse(ann_path)
        root = tree.getroot()

        ann_objects = root.findall(".//object")
        for curr_object in ann_objects:
            obj_class_name = curr_object[0].text
            obj_class = name_to_class[obj_class_name]
            left = float(curr_object[child][0].text)
            top = float(curr_object[child][1].text)
            right = float(curr_object[child][2].text)
            bottom = float(curr_object[child][3].text)

            rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
            label = sly.Label(rect, obj_class)
            labels.append(label)

        # tag_name = (
        #     image_path.split("/")[-2]
        #     if not "plasmodium-images" in image_path
        #     else image_path.split("/")[-3]
        # )
        # # tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == tag_name]

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    name_to_class = {
        "Hookworm": sly.ObjClass("hookworm", sly.Rectangle),
        "Taenia": sly.ObjClass("taenia", sly.Rectangle),
        "Hymenolepsis Nana": sly.ObjClass("hymenolepsis nana", sly.Rectangle),
        "TBbacillus": sly.ObjClass("tb bacillus", sly.Rectangle),
        "plasmodium": sly.ObjClass("plasmodium", sly.Rectangle),
        "person": sly.ObjClass("trophozoite", sly.Rectangle),
    }

    # tag_metas = [sly.TagMeta(name, sly.TagValueType.NONE) for name in os.listdir(dataset_path)]

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=list(name_to_class.values()))
    api.project.update_meta(project.id, meta.to_json())

    all_data = os.listdir(dataset_path)

    for curr_data in all_data:
        curr_dataset_path = os.path.join(dataset_path, curr_data)
        if dir_exists(curr_dataset_path):
            dataset = api.dataset.create(project.id, curr_data, change_name_if_conflict=True)

            if curr_data == "plasmodium-images":
                curr_dataset_path = os.path.join(curr_dataset_path, "images")

            images_names = [
                im_name
                for im_name in os.listdir(curr_dataset_path)
                if get_file_ext(im_name) == images_ext
            ]

            progress = sly.Progress("Create dataset {}".format(curr_data), len(images_names))

            for images_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_pahtes_batch = [
                    os.path.join(curr_dataset_path, im_name) for im_name in images_names_batch
                ]

                img_infos = api.image.upload_paths(
                    dataset.id, images_names_batch, images_pahtes_batch
                )
                img_ids = [im_info.id for im_info in img_infos]

                anns = [create_ann(image_path) for image_path in images_pahtes_batch]
                api.annotation.upload_anns(img_ids, anns)

                progress.iters_done_report(len(images_names_batch))
    return project
