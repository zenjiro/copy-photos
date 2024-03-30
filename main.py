# お気に入りにマークした写真を壁紙フォルダーにコピー
import datetime
import glob
import os
import re
import shutil

import pyexiv2

from config import dcim_dir, pictures_dir, pictures_dir2

if __name__ == "__main__":
    # XXX 「RuntimeError: Directory Canon with 13312 entries considered invalid; not read.」エラーを抑制
    pyexiv2.set_log_level(4)
    latest_timestamp = sorted(
        [
            datetime.datetime.fromtimestamp(os.path.getctime(f"{pictures_dir}/{file}"))
            for file in glob.iglob("*.JPG", root_dir=pictures_dir)
        ]
    )[-1]
    latest_date_time = ""
    for file in glob.iglob("*.JPG", root_dir=pictures_dir):
        timestamp = datetime.datetime.fromtimestamp(
            os.path.getctime(f"{pictures_dir}/{file}")
        )
        if latest_timestamp - timestamp < datetime.timedelta(hours=1):
            with pyexiv2.Image(f"{pictures_dir}/{file}", encoding="CP932") as img:
                latest_date_time = max(
                    latest_date_time, img.read_exif().get("Exif.Image.DateTime", latest_date_time)
                )
    latest_date = re.sub(" .+", "", latest_date_time).replace(":", "_")
    for file in glob.iglob("*/*.JPG", root_dir=dcim_dir):
        dir_name = os.path.dirname(file)
        basename = os.path.basename(file)
        if dir_name >= latest_date:
            with pyexiv2.Image(f"{dcim_dir}/{file}", encoding="CP932") as img:
                rating = int(img.read_xmp()["Xmp.xmp.Rating"]) if "Xmp.xmp.Rating" in img.read_xmp() else -1
                if rating >= 4:
                    date_time = img.read_exif()["Exif.Image.DateTime"]
                    if date_time > latest_date_time:
                        if os.path.isfile(f"{pictures_dir}/{basename}"):
                            splitext = os.path.splitext(basename)
                            for i in range(2, 100):
                                target = (
                                    f"{pictures_dir}/{splitext[0]} ({i}){splitext[1]}"
                                )
                                if not os.path.isfile(target):
                                    print(f"copying {dcim_dir}/{file} to {target}")
                                    shutil.copy2(f"{dcim_dir}/{file}", target)
                                    break
                        else:
                            print(
                                f"copying {dcim_dir}/{file} to {pictures_dir}/{basename}"
                            )
                            shutil.copy2(
                                f"{dcim_dir}/{file}", f"{pictures_dir}/{basename}"
                            )
                        if os.path.isfile(f"{pictures_dir2}/{basename}"):
                            splitext = os.path.splitext(basename)
                            for i in range(2, 100):
                                target = (
                                    f"{pictures_dir2}/{splitext[0]} ({i}){splitext[1]}"
                                )
                                if not os.path.isfile(target):
                                    print(f"copying {dcim_dir}/{file} to {target}")
                                    shutil.copy2(f"{dcim_dir}/{file}", target)
                                    break
                        else:
                            print(
                                f"copying {dcim_dir}/{file} to {pictures_dir2}/{basename}"
                            )
                            shutil.copy2(
                                f"{dcim_dir}/{file}", f"{pictures_dir2}/{basename}"
                            )
