import os
import tarfile


if __name__ == "__main__":
    # Packs Russian-Russian-dict folder into Russian-Russian-dict.tar.gz
    with tarfile.open("Russian-Russian-dict.tar.gz", "w:gz") as tar:
        tar.add("Russian-Russian-dict", arcname=os.path.basename("Russian-Russian-dict"))

