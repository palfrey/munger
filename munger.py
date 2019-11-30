import sys
import time
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import re
import glob
import subprocess

last_update = None
changed = []

class UpdateHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory == False:
            if not event.src_path.endswith(".pnm"):
                return

            print("Path changed", event)
            stat = os.stat(event.src_path)
            global last_update, changed
            if stat.st_mtime > last_update:
                last_update = stat.st_mtime
            changed.append(event.src_path)

def run_cmd(item, rest, ext, cmd_format, stdin_format=None):
    newpath = rest + ext
    if not os.path.exists(newpath):
        print("making", newpath)
        cmd = cmd_format.format(item=item, newpath=newpath, rest=rest)
        print("cmd", cmd)
        if stdin_format == None:
            stdin = None
        else:
            stdin = stdin_format.format(item=item, newpath=newpath, rest=rest)
            print("stdin", stdin)
            stdin = open(stdin)
        ret = subprocess.call(cmd, stdin=stdin, shell=True)
        if ret != 0:
            if os.path.exists(newpath):
                os.remove(newpath)
        assert os.path.exists(newpath)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1]

    for item in os.listdir(path):
        if not item.endswith(".pnm"):
            continue
        fullpath = os.path.join(path,item)
        stat = os.stat(os.path.join(path,item))
        when = stat.st_mtime
        if last_update == None or last_update < when:
            last_update = when
        changed.append(fullpath)
    event_handler = UpdateHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        scan_pattern = re.compile("(scan_\d+-\d+-\d+-\d+)_\d+.pnm")
        while True:
            time_since = time.time()-last_update
            print(time_since)
            if time_since > 3:
                patterns = set()
                while len(changed) > 0:
                    item = changed.pop()
                    if item[0] == ".":
                        continue
                    rest, ext = os.path.splitext(item)
                    print(item)
                    #run_cmd(item, rest, ".tif", "convert \"{item}\" \"{newpath}\"")
                    #run_cmd(item, rest, ".pnm.unpaper", "unpaper \"{item}\" \"{newpath}\"")
                    run_cmd(item, rest, ".tiff", "pamtotiff -output \"{newpath}\" \"{item}\"")
                    #run_cmd(item, rest, ".hocr", "tesseract \"{rest}.tiff\" \"{rest}\" -l eng hocr")
                    #run_cmd(item, rest, ".pdf", "hocr2pdf -i \"{rest}.tiff\" -s -o \"{newpath}\"", stdin_format = "{rest}.hocr")
                    run_cmd(item, rest, ".pdf", "tiff2pdf -o \"{newpath}\" -j -q 95 -p \"A4\" \"{rest}.tiff\"")
                    patt = scan_pattern.search(item)
                    patterns.add(patt.groups()[0])
                for patt in patterns:
                    prefix = os.path.join(path, patt)
                    items = sorted(glob.glob(prefix + "*.pdf"))
                    print(items)
                    cmd = "gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=\"%s.joined.pdf\" %s" % (prefix, " ".join(items))
                    print(cmd)
                    ret = os.system(cmd)
                    if ret != 0:
                        raise Exception
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()