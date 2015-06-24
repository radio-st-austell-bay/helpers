#C:\Users\smst\AppData\Local\Radio Server Player 2>
#for /d %f in (profiles\*) do \code\rsab\nowplaying\copy_ftp.py setup.ini "%f\setup.ini"

start_time = __import__('time').time()

def selective_merge(target_ini, merge_from_ini, merge_items):
    try:
        set
    except NameError:
        from sets import Set as set
    import shutil
    import tempfile
    import time

    fm = open(merge_from_ini, 'r')
    lines_m = fm.readlines()
    fm.close()

    merge_values = {}
    merge_items = set(merge_items)

    seen_sections = set()
    seen_in_this_section = set()
    section = None
    for line in lines_m:
        line = line.strip()
        if not line:
            continue
        if line.startswith('['):
            s = line[1:].split(']')[0]
            if s not in seen_sections:
                section = s
                seen_sections.add(section)
            seen_in_this_section.clear()
            continue
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip()
        if k not in seen_in_this_section:
            seen_in_this_section.add(k)
            if (section, k) in merge_items and (section, k) not in merge_values:
                merge_values[(section, k)] = v

    ft = open(target_ini, 'r')
    lines_t = ft.readlines()
    ft.close()

    out_lines = []

    section = None
    for line in lines_t:
        write_line = line
        line = line.strip()
        if line.startswith('['):
            section = line[1:].split(']')[0]
        elif '=' in line:
            k, v = line.split('=', 1)
            k = k.strip()
            v = v.strip()
            if (section, k) in merge_values:
                write_line = '%s=%s\n' % (k, merge_values[(section, k)])
        out_lines.append(write_line)

    backup_ext = time.strftime('.%Y%m%d-%H%M%S', time.localtime(start_time))
    shutil.move(target_ini, target_ini + backup_ext)
    fw = open(target_ini, 'w')
    for line in out_lines:
        fw.write(line)
    fw.close()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print 'Usage: %s SOURCE_INI TARGET_INI' % (sys.argv[0],)
        sys.exit(0)

    merge_from_ini = sys.argv[1]
    target_ini = sys.argv[2]
    print '%s -> %s' % (merge_from_ini, target_ini)
    selective_merge(
        target_ini,
        merge_from_ini,
        [
            ('player', 'ftpxtra'),
            ('ftp', 'enable'),
            ('ftp', 'server'),
            ('ftp', 'user'),
            ('ftp', 'pass'),
            ('ftp', 'path'),
        ],
    )
