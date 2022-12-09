Search.setIndex({"docnames": ["community_guides", "demo", "index", "installation", "modules", "modules/firmware_update", "modules/hmc_command", "modules/hmc_pwdpolicy", "modules/hmc_update_upgrade", "modules/hmc_user", "modules/power_system", "modules/powervm_dlpar", "modules/powervm_lpar_instance", "modules/powervm_lpar_migration", "modules/vios", "playbooks", "plugins", "plugins/powervm_inventory", "quickstart", "release_notes", "requirements"], "filenames": ["community_guides.rst", "demo.rst", "index.rst", "installation.rst", "modules.rst", "modules/firmware_update.rst", "modules/hmc_command.rst", "modules/hmc_pwdpolicy.rst", "modules/hmc_update_upgrade.rst", "modules/hmc_user.rst", "modules/power_system.rst", "modules/powervm_dlpar.rst", "modules/powervm_lpar_instance.rst", "modules/powervm_lpar_migration.rst", "modules/vios.rst", "playbooks.rst", "plugins.rst", "plugins/powervm_inventory.rst", "quickstart.rst", "release_notes.rst", "requirements.rst"], "titles": ["Contributing", "Demo", "IBM Power Systems HMC Collection for Ansible", "Installation", "Modules", "firmware_update \u2013 Change firmware level on Managed Systems", "hmc_command \u2013 Execute HMC command", "hmc_pwdpolicy \u2013 Manages the list, create, change and remove password policies of the HMC", "hmc_update_upgrade \u2013 Manages the update and upgrade of the HMC", "hmc_user \u2013 Manage the hmc users", "power_system \u2013 PowerOn, PowerOff, modify_syscfg, modify_hwres, facts of the Managed system", "powervm_dlpar \u2013 Dynamically managing resources of partition", "powervm_lpar_instance \u2013 Create, Delete, Shutdown, Activate, Restart, Facts and Install of PowerVM Partitions", "powervm_lpar_migration \u2013 validate, migrate and recover of the LPAR", "vios \u2013 Creation and management of Virtual I/O Server partition", "Playbooks", "Plugins", "powervm_inventory \u2013 HMC-based inventory source for Power Servers", "Quickstart", "Releases", "Requirements"], "terms": {"we": [0, 9, 12, 17], "ar": [0, 3, 5, 8, 9, 10, 11, 12, 15, 17, 18], "current": [0, 7, 8, 9, 11, 12, 17, 18], "accept": [0, 4, 5, 14, 16, 19], "commun": [0, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18], "howev": [0, 20], "encourag": 0, "you": [0, 2, 3, 15, 17, 18, 20], "open": [0, 2], "git": [0, 3], "issu": [0, 17], "bug": 0, "comment": 0, "featur": [0, 3, 17], "request": 0, "review": [0, 3, 15], "thi": [0, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18], "content": [0, 1, 3, 15, 18], "period": [0, 3], "learn": 0, "when": [0, 3, 5, 7, 8, 9, 10, 12, 15, 17], "how": [0, 1, 3, 15, 18], "make": [0, 3, 10, 12], "futur": 0, "ansibl": [0, 4, 8, 15, 16, 17, 20], "guid": [0, 18], "ibm": [0, 1, 3, 4, 5, 6, 15, 16, 17, 20], "knowledg": [0, 17], "center": [0, 17], "follow": [1, 3, 4, 8, 15, 17, 18], "set": [1, 3, 7, 8, 9, 10, 11, 12, 14, 17, 19], "exampl": [1, 3, 15, 18], "scenario": 1, "demonstr": [1, 3, 15], "modul": [1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19], "hmc": [1, 3, 4, 5, 10, 11, 12, 13, 14, 16, 18, 19, 20], "collect": [1, 3, 4, 15, 16, 18, 19, 20], "The": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20], "gif": 1, "from": [1, 2, 3, 7, 8, 9, 12, 13, 15, 17, 18, 19, 20], "v9": [1, 8, 12], "r1": [1, 8, 12], "m910": [1, 8], "m941": 1, "disk": [1, 8, 12, 18, 19], "sourc": [1, 2, 3, 12, 13, 15, 16], "which": [1, 8, 10, 12, 15, 17], "take": [1, 15], "imag": [1, 5, 8, 19], "control": [1, 3, 4, 8, 15, 16, 18], "node": [1, 3, 4, 8, 15, 16, 18], "v8": [1, 8], "r870": [1, 8], "through": [1, 2, 12, 14, 17], "nf": [1, 8, 18], "server": [1, 2, 4, 5, 8, 9, 11, 12, 16, 18, 19, 20], "password": [1, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 17, 19], "polici": [1, 4, 10, 19], "illustr": [1, 12], "usag": 1, "It": [1, 15], "input": [1, 13], "iter": 1, "here": [1, 3, 18], "each": [1, 4, 15, 16], "task": [1, 2, 4, 8, 15, 16, 18], "care": [1, 15], "remov": [1, 4, 8, 9, 12], "map": [1, 3, 12], "vdisk": [1, 19], "associ": [1, 5, 12, 17], "well": 1, "case": [1, 5, 8, 17, 18], "memori": [1, 10, 11, 12, 19], "share": [1, 11, 12, 19], "processor": [1, 11, 12, 19], "along": [1, 3], "storag": [1, 12, 19], "network": [1, 8, 12, 14, 19], "configur": [1, 2, 3, 7, 8, 9, 10, 12, 14, 19], "onc": [1, 15], "default": [1, 3, 5, 9, 12, 14, 17, 18], "profil": [1, 12, 14], "list": [1, 4, 8, 9, 12, 13, 15, 17, 20], "down": 1, "detail": [1, 9, 10, 12, 14, 15, 17, 19], "chang": [1, 3, 4, 8, 9, 10], "like": [1, 7, 12, 18], "name": [1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18], "poweron": [1, 4, 12], "resourc": [1, 4, 9, 10, 12, 15, 19], "region": [1, 10], "size": [1, 10, 12, 17], "huge": [1, 10], "page": [1, 10, 18], "user": [1, 3, 4, 5, 8, 10, 12, 14, 15, 17], "provid": [1, 2, 3, 8, 9, 12, 13, 14, 15, 18], "ioslot": 1, "newli": 1, "nim": [1, 12, 14], "after": [1, 3, 8, 10, 12, 14, 18], "success": [1, 9, 12, 14], "can": [2, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 17, 18, 20], "us": [2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], "manag": [2, 4, 12, 13, 15, 17, 18, 19], "hardwar": [2, 7, 9, 10], "consol": [2, 3, 7, 9, 13, 15], "help": [2, 15], "includ": [2, 3, 7, 15, 17, 18, 19], "part": 2, "enterpris": 2, "autom": [2, 3, 4, 16], "strategi": 2, "ecosystem": 2, "i": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17, 18, 19, 20], "famili": 2, "transform": 2, "your": [2, 3, 15, 17, 18], "organ": [2, 15], "deliv": 2, "industri": 2, "lead": 2, "resili": 2, "scalabl": 2, "acceler": 2, "perform": [2, 4, 8, 9, 13, 17, 18], "most": [2, 17], "sensit": 2, "mission": 2, "critic": 2, "workload": 2, "next": [2, 10, 12], "gener": [2, 6, 17, 19], "ai": 2, "edg": 2, "solut": [2, 18], "platform": [2, 3], "also": [2, 9, 12, 17], "leverag": 2, "technologi": 2, "enabl": [2, 3, 9, 17], "run": [2, 17, 20], "hybrid": 2, "cloud": 2, "environ": [2, 15, 17], "consist": [2, 15, 17], "tool": [2, 3], "process": [2, 3, 11, 12], "skill": 2, "broader": 2, "offer": 2, "avail": [2, 3, 12, 14, 15, 19], "galaxi": [2, 19], "ha": [2, 12, 15], "support": [2, 3, 8, 9, 10, 11, 12, 14, 15, 17, 19], "sampl": [2, 3], "playbook": [2, 3, 4, 16, 17, 18, 20], "aix": [2, 12, 17, 19], "corpor": 2, "2020": 2, "under": 2, "gnu": 2, "public": [2, 15], "version": [2, 3, 12, 20], "3": [2, 5, 8, 11, 12, 17, 20], "0": [2, 3, 9, 12, 14, 17, 20], "maintain": [2, 6, 7, 8, 9, 10, 11, 12, 13, 14], "develop": 2, "team": 2, "power": [3, 4, 10, 15, 16, 18, 19, 20], "system": [3, 4, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "one": [3, 9, 12, 13], "option": [3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 19], "For": [3, 8, 13, 15, 18], "more": [3, 9, 12, 14, 15, 17, 18, 19], "inform": [3, 6, 7, 8, 9, 10, 12, 13, 14, 15, 17, 18], "see": 3, "quickli": 3, "project": 3, "prepackag": 3, "unit": [3, 11, 12, 19], "work": [3, 10, 11, 12, 15, 17, 18], "known": [3, 12, 15, 17], "command": [3, 4, 14, 15, 18, 19, 20], "host": [3, 5, 8, 12, 13, 15, 17, 18, 19, 20], "By": [3, 12, 17, 18], "latest": [3, 5], "add": [3, 12, 13, 17], "identifi": [3, 12, 15, 17], "specif": [3, 5, 13, 20], "befor": [3, 7, 15], "all": [3, 6, 7, 9, 10, 12, 13, 14, 15, 17, 18, 19], "new": [3, 7, 9, 10], "releas": [3, 8, 12, 15], "contain": [3, 4, 5, 7, 8, 15, 16], "enhanc": [3, 19], "might": 3, "interest": 3, "becom": 3, "ignor": [3, 12, 19], "ani": [3, 6, 7, 8, 12, 17, 20], "pre": 3, "unless": 3, "rang": 3, "A": [3, 7, 15, 17, 20], "denot": 3, "append": [3, 15], "hyphen": 3, "seri": 3, "dot": 3, "separ": [3, 12, 13, 17], "immedi": 3, "patch": [3, 19], "convent": 3, "1": [3, 9, 10, 12], "beta1": 3, "would": [3, 12, 18], "requir": [3, 5, 7, 15, 18], "an": [3, 5, 8, 9, 12, 15, 17, 18], "power_hmc": [3, 5, 15, 17], "If": [3, 11, 12, 13, 14, 17], "have": [3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18], "prior": [3, 7, 12], "must": [3, 7, 9, 15, 17], "overwrit": 3, "exist": [3, 8, 12], "forc": 3, "few": 3, "f": 3, "progress": 3, "output": [3, 6, 17], "note": [3, 15, 19], "locat": [3, 5, 8, 12, 14, 15, 18], "so": [3, 17], "other": [3, 13], "depend": [3, 17], "start": [3, 9, 10], "ansible_collect": [3, 15, 18], "resembl": [3, 17], "hierarchi": 3, "doc": [3, 6], "plugin": [3, 15, 17, 18, 19], "module_util": 3, "p": 3, "specifi": [3, 9, 10, 12, 13, 14, 15, 17], "path": [3, 8, 12, 15], "home": 3, "valu": [3, 4, 15, 16, 17], "collections_path": 3, "where": [3, 5, 8, 15], "itself": [3, 15], "expect": [3, 4, 12, 15, 16], "find": [3, 15], "built": 3, "directori": [3, 5, 9, 15], "repositori": [3, 5], "archiv": 3, "without": [3, 15, 17, 18], "To": [3, 9, 12, 13, 14, 15, 17], "obtain": [3, 8, 15, 18], "copi": 3, "thei": [3, 17], "adher": 3, "namespac": [3, 18], "tar": 3, "gz": 3, "In": [3, 15, 18], "access": [3, 5, 9, 15, 18], "publish": 3, "unlik": 3, "mai": [3, 17], "need": [3, 5, 8, 12, 15, 17, 18], "creat": [3, 4, 9, 11, 14, 15, 17, 19], "custom": [3, 9, 15], "ee": 3, "packag": [3, 8, 18], "base": [3, 9, 12, 15, 16, 18, 19], "univers": 3, "step": 3, "2": [3, 11, 12, 17, 18, 20], "x": 3, "setup": 3, "machin": [3, 15, 18, 20], "builder": 3, "refer": [3, 15, 18, 20], "offici": 3, "document": [3, 4, 16, 17, 18], "yaml": [3, 17], "sure": [3, 12], "file": [3, 5, 8, 15, 18], "present": [3, 7, 9, 12, 14], "t": [3, 8, 12, 14], "image_tag": 3, "execut": [4, 5, 8, 12, 15, 16, 17, 18], "target": [4, 5, 7, 8, 15, 16, 17, 20], "return": [4, 16], "result": [4, 16, 17], "back": [4, 12, 16], "while": [4, 12, 14], "differ": 4, "interfac": [4, 6, 7, 8, 9, 10, 11, 12, 13, 14], "respons": 4, "similar": [4, 15, 18], "pattern": [4, 12, 15, 17], "materi": [4, 16], "paramet": [4, 16], "firmware_upd": 4, "firmwar": 4, "level": [4, 8, 12, 15, 18, 19, 20], "hmc_command": [4, 19], "hmc_pwdpolici": 4, "hmc_update_upgrad": [4, 18, 19], "updat": [4, 5, 7, 9, 11, 18, 19], "upgrad": [4, 5, 18, 19], "hmc_user": 4, "power_system": [4, 19], "poweroff": 4, "modify_syscfg": 4, "modify_hwr": 4, "fact": [4, 7, 8, 9, 14, 18, 19], "powervm_dlpar": 4, "dynam": [4, 17, 19], "partit": [4, 8, 10, 13, 17, 18, 19], "powervm_lpar_inst": [4, 19], "delet": [4, 19], "shutdown": [4, 10, 19], "activ": [4, 5, 7, 19], "restart": [4, 10], "instal": [4, 8, 14, 15, 18, 19, 20], "powervm": [4, 11], "powervm_lpar_migr": [4, 19], "valid": [4, 5, 7, 8, 9, 11, 12, 14, 17], "migrat": [4, 19], "recov": 4, "lpar": [4, 10, 12, 17], "vio": [4, 12, 17, 19], "creation": [4, 12, 19], "virtual": [4, 11, 12, 17, 19], "o": [4, 12, 17, 19], "hmc_host": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19], "true": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "str": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "none": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "ip": [5, 6, 9, 11, 12, 13, 14, 17], "address": [5, 6, 9, 11, 12, 13, 14, 17], "hostnam": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "hmc_auth": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18], "dict": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "usernam": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18], "credenti": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "system_nam": [5, 10, 11, 12, 14], "ibmwebsit": 5, "type": [5, 8, 9, 12, 17, 18], "remote_repo": 5, "remot": [5, 8, 9, 13, 15, 18], "userid": [5, 8], "id": [5, 8, 9, 11, 12, 13], "log": [5, 8, 9, 15], "ftp": [5, 8, 18], "sftp": [5, 8, 18], "otherwis": [5, 8], "passwd": [5, 8, 9], "sshkei": [5, 8], "mutual": [5, 8, 12], "exclus": [5, 8, 12, 17], "location_typ": [5, 8], "onli": [5, 7, 8, 9, 10, 12, 13, 14, 17], "sshkey_fil": [5, 8], "ssh": [5, 8, 9, 13, 15, 18, 19], "privat": [5, 8], "kei": [5, 8, 13, 15, 17, 19], "store": [5, 15], "oper": [5, 8, 9, 11, 12, 13, 15, 17, 18], "state": [5, 7, 8, 9, 10, 12, 14, 17, 18, 19], "action": [5, 9, 10, 11, 12, 13, 14], "inventory_hostnam": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18], "ansible_us": [5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 18], "hmc_password": [5, 6, 7, 8, 10, 11, 12, 13, 14, 17], "repo": 5, "curr_hmc_auth": [5, 12], "mtm": 5, "9": [5, 18, 20], "147": 5, "210": 5, "01vl941_047": 5, "service_pack": 5, "alwai": [5, 6, 7, 8, 10, 11, 12, 13, 15], "fw940": 5, "20": [5, 9, 12], "servic": [5, 8, 18], "pack": 5, "represent": 5, "55": 5, "ecnumb": 5, "01vl940": 5, "engin": 5, "ec": 5, "number": [5, 7, 9, 10, 11, 12], "mario": 5, "maldonado": 5, "mariomd": 5, "cli": [6, 19], "given": [6, 8, 12, 17], "select": [6, 15], "about": [6, 15, 17], "found": [6, 17], "http": 6, "www": 6, "com": 6, "en": 6, "power10": 6, "7063": 6, "cr1": 6, "topic": [6, 18], "login": [6, 7, 8, 9, 10, 11, 13, 14, 15], "cmd": 6, "command_output": [6, 9], "respect": [6, 7, 8, 9, 10, 13, 14], "guarante": [6, 7, 8, 9, 10, 11, 12, 13, 14], "backward": [6, 7, 8, 9, 10, 11, 12, 13, 14], "compat": [6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "preview": [6, 7, 8, 9, 10, 11, 12, 13, 14], "navinakumar": [6, 8, 9, 10, 12, 13, 14, 17], "kandakur": [6, 8, 10, 12, 13, 14, 17], "nkandak1": [6, 8, 9, 10, 12, 13, 14, 17], "deactiv": 7, "modifi": [7, 9, 10], "ipaddress": [7, 8, 10, 12, 13], "policy_nam": 7, "policy_config": 7, "pwage": [7, 9], "dai": [7, 9], "elaps": 7, "expir": 7, "99999": [7, 9], "indic": [7, 9], "descript": [7, 9, 12], "min_pwag": [7, 9], "warn_pwag": 7, "warn": [7, 12, 15], "messag": 7, "begin": 7, "displai": [7, 12, 14, 17], "min_length": 7, "minimum": [7, 12], "length": 7, "hist_siz": 7, "time": [7, 9, 11, 12, 13, 14, 15, 17], "reus": 7, "cannot": [7, 20], "exce": 7, "50": [7, 12], "min_digit": 7, "digit": 7, "min_uppercase_char": 7, "uppercas": 7, "charact": 7, "min_lowercase_char": 7, "lowercas": 7, "min_special_char": 7, "special": [7, 8, 18], "symbol": 7, "punctuat": 7, "white": 7, "space": [7, 15], "new_nam": [7, 9, 10], "policy_typ": 7, "desir": [7, 8, 9], "ensur": [7, 8, 9, 15], "mention": [7, 12, 15], "absent": [7, 9, 12], "doe": [7, 8, 9], "anyth": [7, 8, 9], "dummi": 7, "80": 7, "12": 7, "de": 7, "policy_info": 7, "anil": [7, 8, 9, 10, 11, 12, 14, 17], "vijayan": [7, 8, 9, 10, 11, 12, 14, 17], "anilvijayan": [7, 8, 9, 10, 11, 12, 14, 17], "correct": [8, 18], "hard": [8, 18], "transfer": [8, 18], "onto": [8, 18], "been": [8, 12, 18], "boot": [8, 18], "below": [8, 12, 17, 20], "python": [8, 12, 17, 20], "build_config": 8, "fals": [8, 9, 12, 17], "iso": 8, "site": 8, "secur": [8, 9], "first": [8, 12, 14], "look": 8, "build_fil": 8, "doesn": [8, 12, 14], "mount_loc": 8, "mount": 8, "defin": [8, 12, 14, 15, 17], "filesystem": 8, "dure": [8, 9, 12, 14, 15, 19], "repres": 8, "kept": 8, "should": [8, 9, 12, 14, 15, 17], "build": [8, 17, 18], "driver": 8, "local": [8, 9, 15, 18, 19], "won": 8, "satisfi": 8, "idempot": 8, "even": 8, "though": 8, "partial": 8, "confirm": 8, "instanc": [8, 12], "same": [8, 13, 15], "still": 8, "go": 8, "ahead": 8, "final": 8, "report": 8, "v9r1m941": 8, "nfs_server_ip": 8, "hmc_update_v9r1m941_x86": 8, "hmcimag": 8, "sftp_server_ip": 8, "sftp_server_usernam": 8, "sftp_server_password": 8, "build_info": 8, "ldap": 9, "ldap_fact": 9, "enable_us": 9, "bool": [9, 12, 13, 17], "wa": [9, 18], "disabl": 9, "due": 9, "inact": [9, 12], "kerbero": 9, "automanag": 9, "filter": [9, 17], "out": [9, 17], "particular": 9, "ldap_resourc": 9, "remove_ldap_config": 9, "attribut": [9, 11, 14, 17], "taskrol": 9, "hmcsuperadmin": 9, "hmcoper": 9, "hmcviewer": 9, "hmcpe": 9, "hmcservicerep": 9, "hmcclientliveupd": 9, "role": [9, 12], "resourcerol": 9, "current_passwd": 9, "": [9, 12, 13, 15, 17, 18], "authentication_typ": 9, "session_timeout": 9, "int": [9, 10, 11, 12, 13, 14], "minut": [9, 11, 13], "verify_timeout": 9, "15": 9, "idle_timeout": 9, "120": 9, "inactivity_expir": 9, "remote_webui_access": 9, "allow": [9, 13, 15, 17, 18], "web": 9, "remote_ssh_access": 9, "passwd_authent": 9, "remote_user_nam": 9, "max_webui_login_attempt": 9, "maximum": [9, 11, 12, 13], "ui": 9, "attempt": 9, "webui_login_suspend_tim": 9, "ldap_set": 9, "primari": 9, "backup": 9, "basedn": 9, "dn": 9, "search": 9, "binddn": 9, "bind": 9, "non": [9, 17], "anonym": 9, "bindpw": 9, "timelimit": 9, "limit": [9, 15], "second": [9, 17], "bindtimelimit": 9, "whether": 9, "automat": [9, 12, 14, 17], "authent": [9, 13], "auth": 9, "loginattribut": 9, "hmcuserpropsattribut": 9, "retriev": [9, 17], "properti": [9, 17], "hmcauthnameattribut": 9, "searchfilt": 9, "scope": 9, "referr": 9, "chase": 9, "starttl": 9, "transport": 9, "layer": 9, "tl": 9, "hmcgroup": 9, "group": [9, 15, 17], "authsearch": 9, "addit": [9, 15, 17, 18], "con": 9, "firmat": 9, "tlsreqcert": 9, "what": [9, 15], "check": 9, "suppli": 9, "certif": 9, "groupattribut": 9, "member": 9, "memberattribut": 9, "configure_ldap": 9, "light": 9, "weight": [9, 11, 12], "protocol": [9, 18], "client": [9, 12], "user_nam": 9, "new_user_password": 9, "new_user_nam": 9, "hmc_user_nam": 9, "primary_url": 9, "bind_pwd": 9, "ou": 9, "peopl": 9, "dc": 9, "url": 9, "cn": 9, "resource_nam": 9, "except": 9, "c": [9, 12], "kandaur": 9, "get": [10, 17], "power_off_polici": 10, "off": 10, "power_on_lpar_start_polici": 10, "requested_num_sys_huge_pag": 10, "mem_mirroring_mod": 10, "mirror": 10, "mode": [10, 11, 12, 15], "pend_mem_region_s": 10, "choic": 10, "mb": [10, 12], "fetch": [10, 12, 14, 17, 19], "managed_system_nam": [10, 13, 14], "managed_sysystem_nam": 10, "system_name_to_be_chang": 10, "autostart": 10, "sys_huge_pages_to_be_set": 10, "sys_firmware_onli": 10, "auto": [10, 12], "system_info": [10, 13], "vm_name": [11, 12, 13], "proc_set": 11, "relat": 11, "proc": [11, 12, 19], "dedic": [11, 12, 19], "proc_unit": [11, 12], "float": [11, 12], "sharing_mod": 11, "keep_idle_proc": 11, "share_idle_proc": 11, "share_idle_procs_act": 11, "share_idle_procs_alwai": 11, "cap": [11, 12], "uncap": [11, 12], "uncapped_weight": 11, "pool_id": 11, "pool": [11, 12, 19], "mem_set": 11, "mem": [11, 12, 19], "megabyt": [11, 12], "timeout": [11, 12, 14], "wait": [11, 12, 13, 14], "complet": [11, 13], "dlpar": 11, "vm": 11, "5": 11, "131": 11, "3072": 11, "partition_info": [11, 12], "linux": [12, 17, 19], "ibmi": [12, 17, 19], "Or": [12, 15], "lxml": 12, "vm_id": [12, 13], "logic": 12, "assign": [12, 19], "max_proc": 12, "max": [12, 14], "equal": 12, "greater": 12, "than": [12, 14], "min_proc": 12, "min": [12, 14], "less": [12, 15], "shared_proc_pool": 12, "numer": 12, "consid": 12, "defaultpool": 12, "max_proc_unit": 12, "min_proc_unit": 12, "proc_mod": 12, "128": 12, "proc_compatibility_mod": 12, "2048": 12, "max_mem": 12, "min_mem": 12, "1024": 12, "os_typ": 12, "aix_linux": 12, "prof_nam": [12, 14], "keylock": 12, "posit": 12, "iiplsourc": 12, "initi": 12, "program": 12, "load": 12, "ipl": 12, "give": 12, "proce": 12, "volume_config": 12, "volum": [12, 19], "attach": [12, 14], "physic": [12, 19], "via": [12, 18], "scsi": 12, "redund": 12, "visibl": 12, "either": [12, 15, 17], "volume_s": 12, "both": 12, "volume_nam": 12, "vios_nam": 12, "match": [12, 17], "virt_network_config": 12, "implicitli": 12, "ethernet": [12, 14], "adapt": [12, 14, 19], "bridg": 12, "extern": 12, "network_nam": 12, "mandatori": [12, 13], "slot_numb": 12, "slot": [12, 19], "npiv_config": 12, "n": 12, "port": [12, 15], "fibr": [12, 19], "two": [12, 17], "fc": 12, "fc_port": 12, "npiv": [12, 19], "fulli": [12, 14, 18], "qualifi": [12, 18], "code": [12, 14, 18], "wwpn_pair": 12, "wwpn": [12, 19], "pair": [12, 17], "semicolon": 12, "delimit": 12, "client_adapter_id": 12, "server_adapter_id": 12, "all_resourc": 12, "choos": [12, 17], "max_virtual_slot": 12, "physical_io": 12, "io": [12, 17, 19], "ad": [12, 15, 17, 18, 19], "xxxxx": 12, "xxx": [12, 17], "xxxxxxx": 12, "p1": 12, "t1": 12, "retain_vios_cfg": 12, "do": [12, 17], "applic": [12, 15], "delete_vdisk": 12, "advanced_info": 12, "advanc": [12, 17], "show": 12, "install_set": 12, "pull": 12, "vm_ip": 12, "nim_ip": [12, 14], "nim_gatewai": [12, 14], "gatewai": [12, 14], "nim_subnetmask": [12, 14], "subnetmask": [12, 14], "location_cod": [12, 14], "pick": [12, 14], "pingabl": [12, 14], "nim_vlan_id": [12, 14], "vlanid": [12, 14], "4094": [12, 14], "tag": [12, 14, 17], "frame": [12, 14], "nim_vlan_prior": [12, 14], "vlan": [12, 14], "prioriti": [12, 14], "7": [12, 14, 17, 20], "bootup": [12, 14], "10": [12, 14, 17], "60": [12, 14], "vnic_config": 12, "nic": 12, "vnic_adapter_id": 12, "vnic": 12, "backing_devic": 12, "sriov": 12, "devic": 12, "link": 12, "up": [12, 15], "randomli": 12, "capac": 12, "hosting_partit": 12, "random": 12, "rmc": [12, 17], "install_o": 12, "abov": [12, 15], "m930": 12, "951": 12, "physicaio": 12, "lpar_id": 12, "4": 12, "20480": 12, "viosname1": 12, "volumename1": 12, "viosname2": 12, "volumename2": 12, "physicalio": 12, "volumes_s": 12, "disk_siz": 12, "virtual_nw_nam": 12, "client_slot_no": 12, "viosnam": 12, "fc_port_nam": 12, "loc_cod": 12, "wwpn1": 12, "wwpn2": 12, "t2": 12, "t3": 12, "t4": 12, "profile_nam": [12, 14], "its": [12, 15, 18], "normal": 12, "d": 12, "ip_address": 12, "ip_addr": 12, "allocatedvirtualprocessor": 12, "associatedmanagedsystem": 12, "currentmemori": [12, 17], "currentprocessingunit": 12, "currentprocessor": 12, "hasdedicatedprocessor": 12, "hasphysicalio": 12, "isvirtualserviceattentionledon": 12, "lastactivatedprofil": 12, "default_profil": [12, 14], "memorymod": 12, "migrationst": 12, "not_migr": 12, "operatingsystemvers": [12, 17], "unknown": [12, 17], "partitionid": 12, "11": 12, "partitionnam": [12, 17], "partitionst": [12, 17], "partitiontyp": [12, 17], "powermanagementmod": 12, "progressst": 12, "rmcstate": 12, "referencecod": 12, "remoterestartst": 12, "invalid": 12, "resourcemonitoringipaddress": 12, "sharingmod": 12, "sre": 12, "idl": 12, "src_system": 13, "dest_system": 13, "destin": 13, "multipl": [13, 15, 17, 19], "comma": 13, "form": 13, "all_vm": 13, "remote_ip": 13, "remote_usernam": 13, "remote_passwd": 13, "destination_managed_system": 13, "vm_name1": 13, "vm_name2": 13, "failur": 13, "id1": 13, "cec": 13, "destination_system_nam": 13, "licens": 14, "virtualioserv": 14, "variou": [14, 17], "mksyscfg": 14, "vios_ip": 14, "accept_licens": 14, "fresh": 14, "vios_partition_nam": 14, "profilenam": 14, "io_slot": 14, "ioslot1": 14, "ioslot2": 14, "vios_info": 14, "instruct": 15, "some": [15, 17], "modif": 15, "ones": 15, "These": [15, 17], "sever": 15, "behavior": 15, "preced": 15, "rule": 15, "cfg": 15, "overrid": 15, "almost": 15, "write": 15, "temporari": 15, "easili": 15, "done": 15, "read": 15, "want": 15, "against": [15, 17], "But": 15, "deviat": 15, "standard": 15, "sinc": [15, 18], "close": [15, 18], "applianc": [15, 18], "restrict": [15, 18], "shell": [15, 18], "wont": 15, "push": [15, 18], "henc": [15, 18], "happen": 15, "handl": 15, "connect": 15, "insid": 15, "instead": [15, 17], "littl": 15, "hmc01": 15, "hmc02": 15, "var": [15, 17], "hscroot": 15, "magic": 15, "variabl": [15, 17], "within": 15, "syntax": 15, "demo_hmc_upd": 15, "yml": [15, 17], "never": 15, "plain": 15, "text": 15, "vault": 15, "mkauthkei": 15, "public_kei": 15, "passwordless": 15, "demo_passwordless_setup": 15, "situat": 15, "fail": 15, "adjust": 15, "letter": 15, "v": 15, "vv": 15, "vvv": 15, "vvvv": 15, "increas": [15, 17], "tradit": 15, "info": [15, 19], "error": 15, "debug": 15, "good": 15, "practic": 15, "them": [15, 17], "understand": 15, "term": 15, "author": 15, "artifact": 15, "clean": 15, "although": 15, "written": 15, "flexibl": 15, "becaus": 15, "easi": 15, "determin": [15, 17], "section": 15, "powervm_inventori": 16, "inventori": [16, 19], "util": 17, "api": 17, "structur": 17, "usabl": 17, "expos": 17, "wai": 17, "identif": 17, "composit": 17, "rest": 17, "those": 17, "quick": 17, "advanced_field": 17, "abl": 17, "further": 17, "system_group": 17, "system_keyed_group": 17, "system_filt": 17, "system_composit": 17, "group_lpars_by_managed_system": 17, "apart": 17, "associatedgroup": 17, "associatedhmc": 17, "associatedhmcusernam": 17, "compos": 17, "uniqu": 17, "maagedsystem": 17, "belong": 17, "jinja2": 17, "express": 17, "system_compos": 17, "condit": 17, "keyed_group": 17, "exclude_ip": 17, "exclud": 17, "compar": 17, "lookup": 17, "exclude_lpar": 17, "exclude_system": 17, "discov": 17, "ansible_display_nam": 17, "wish": 17, "ansible_host_typ": 17, "ansible_host": 17, "purpos": 17, "could": 17, "identify_unknown_bi": 17, "omit": 17, "unabl": 17, "detect": 17, "event": 17, "call": 17, "uuid": 17, "common": 17, "avoid": 17, "targetgroup": 17, "minim": 17, "singl": 17, "hmc_host_nam": 17, "hmc_usernam": 17, "import": 17, "hmc1_usernam": 17, "hmc1_password": 17, "hmc2_usernam": 17, "hmc2_password": 17, "aix_72": 17, "prefix": 17, "type_": 17, "type_virtual_io_serv": 17, "type_aix_linux": 17, "type_os400": 17, "etc": 17, "addition": 17, "host_var": 17, "current_memori": 17, "hmcip": 17, "hmcusernam": 17, "44": 17, "46": [17, 19], "aixlparnamex1": 17, "aixlparnamex2": 17, "vioslparnamex1": 17, "vioslparnamex2": 17, "frame1": 17, "wwwwww": 17, "frame2": 17, "systemtyp": 17, "type_fsp": 17, "type_ebmc": 17, "maximumpartit": 17, "systemfirmwar": 17, "systemnam": 17, "maximum_partit": 17, "system_firmwar": 17, "seper": 17, "production_lpar": 17, "production_system": 17, "productionlpar": 17, "productionsystem": 17, "torin": 17, "reilli": 17, "torinreilli": 17, "michael": 17, "cohoon": 17, "mtcohoon": 17, "ozzi": 17, "rodriguez": 17, "ozzierodriguez": 17, "outlin": 18, "cover": 18, "referenc": 18, "queri": 18, "keyword": 18, "reduc": 18, "repeatedli": 18, "unix": 18, "man": 18, "manual": 18, "line": 18, "py": 18, "over": 18, "nativ": 18, "openssh": 18, "tunnel": 18, "model": 18, "recoveri": 19, "sp": 19, "ptf": 19, "v1": 19, "github": 19, "vconfig": 19, "fix": 19, "incorrectli": 19, "jinja": 19, "templat": 19, "param": 19, "full": 19, "reboot": 19, "cycl": 19, "config": 19, "live": 19, "mobil": 19, "47": 19, "cross": 19, "env": 19, "laptop": 20, "desktop": 20, "window": 20, "often": 20, "softwar": 20, "later": 20, "v8r8": 20, "v9r1": 20}, "objects": {}, "objtypes": {}, "objnames": {}, "titleterms": {"contribut": 0, "help": 0, "link": 0, "demo": 1, "hmc_update_upgrad": [1, 8], "updat": [1, 8], "upgrad": [1, 8], "hmc_pwdpolici": [1, 7], "creat": [1, 7, 12], "activ": [1, 12], "deactiv": 1, "modifi": 1, "powervm_inventori": [1, 17], "delet": [1, 12], "multipl": 1, "inact": 1, "partit": [1, 11, 12, 14], "us": 1, "dynam": [1, 11], "inventori": [1, 15, 17], "plugin": [1, 16], "powervm_lpar_inst": [1, 12], "lpar": [1, 13], "instanc": 1, "power_system": [1, 10], "poweroff": [1, 10], "power": [1, 2, 17], "system": [1, 2, 5, 10], "vio": [1, 14], "instal": [1, 3, 12], "accept": 1, "licens": [1, 2], "ibm": [2, 18], "hmc": [2, 6, 7, 8, 9, 15, 17], "collect": 2, "ansibl": [2, 3, 18], "content": [2, 4, 16], "featur": 2, "copyright": 2, "author": [2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "inform": 2, "galaxi": 3, "local": 3, "build": 3, "execut": [3, 6], "environ": 3, "imag": 3, "modul": 4, "refer": [4, 16], "firmware_upd": 5, "chang": [5, 7], "firmwar": 5, "level": 5, "manag": [5, 7, 8, 9, 10, 11, 14, 20], "synopsi": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "paramet": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "exampl": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "return": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "valu": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "statu": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17], "hmc_command": 6, "command": 6, "list": 7, "remov": 7, "password": [7, 15], "polici": 7, "requir": [8, 12, 17, 20], "note": [8, 12], "hmc_user": 9, "user": 9, "poweron": 10, "modify_syscfg": 10, "modify_hwr": 10, "fact": [10, 12], "powervm_dlpar": 11, "resourc": 11, "shutdown": 12, "restart": 12, "powervm": 12, "powervm_lpar_migr": 13, "valid": 13, "migrat": 13, "recov": 13, "creation": 14, "virtual": 14, "i": 14, "o": 14, "server": [14, 17], "playbook": 15, "document": 15, "sampl": 15, "configur": 15, "setup": 15, "run": 15, "set": 15, "verbos": 15, "base": 17, "sourc": 17, "quickstart": 18, "power_hmc": 18, "doc": 18, "connect": 18, "method": 18, "releas": 19, "version": 19, "1": 19, "0": 19, "2": 19, "3": 19, "4": 19, "5": 19, "control": 20, "node": 20}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 8, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx": 57}, "alltitles": {"Contributing": [[0, "contributing"]], "Helpful Links": [[0, "helpful-links"]], "Demo": [[1, "demo"]], "hmc_update_upgrade": [[1, "hmc-update-upgrade"]], "Update": [[1, "update"]], "Upgrade": [[1, "upgrade"]], "hmc_pwdpolicy": [[1, "hmc-pwdpolicy"]], "Create and Activate": [[1, "create-and-activate"]], "Deactivate, Modify and Activate": [[1, "deactivate-modify-and-activate"]], "powervm_inventory": [[1, "powervm-inventory"]], "Deletion of multiple inactive partitions using dynamic inventory plugin": [[1, "deletion-of-multiple-inactive-partitions-using-dynamic-inventory-plugin"]], "powervm_lpar_instance": [[1, "powervm-lpar-instance"]], "Create and Activate lpar instance": [[1, "create-and-activate-lpar-instance"]], "power_system": [[1, "power-system"]], "Poweroff, Modify and Power on power system": [[1, "poweroff-modify-and-power-on-power-system"]], "vios": [[1, "vios"]], "Create and Install vios then accept license": [[1, "create-and-install-vios-then-accept-license"]], "IBM Power Systems HMC Collection for Ansible": [[2, "ibm-power-systems-hmc-collection-for-ansible"]], "Ansible Content for IBM Power Systems": [[2, "ansible-content-for-ibm-power-systems"]], "Features": [[2, "features"]], "Copyright": [[2, "copyright"]], "License": [[2, "license"]], "Author Information": [[2, "author-information"]], "Installation": [[3, "installation"]], "Ansible Galaxy": [[3, "ansible-galaxy"]], "Local build": [[3, "local-build"]], "Build Execution Environment Image": [[3, "build-execution-environment-image"]], "Modules": [[4, "modules"]], "Module reference": [[4, "module-reference"]], "Contents:": [[4, null], [16, null]], "firmware_update \u2013 Change firmware level on Managed Systems": [[5, "firmware-update-change-firmware-level-on-managed-systems"]], "Synopsis": [[5, "synopsis"], [6, "synopsis"], [7, "synopsis"], [8, "synopsis"], [9, "synopsis"], [10, "synopsis"], [11, "synopsis"], [12, "synopsis"], [13, "synopsis"], [14, "synopsis"], [17, "synopsis"]], "Parameters": [[5, "parameters"], [6, "parameters"], [7, "parameters"], [8, "parameters"], [9, "parameters"], [10, "parameters"], [11, "parameters"], [12, "parameters"], [13, "parameters"], [14, "parameters"], [17, "parameters"]], "Examples": [[5, "examples"], [6, "examples"], [7, "examples"], [8, "examples"], [9, "examples"], [10, "examples"], [11, "examples"], [12, "examples"], [13, "examples"], [14, "examples"], [17, "examples"]], "Return Values": [[5, "return-values"], [6, "return-values"], [7, "return-values"], [8, "return-values"], [9, "return-values"], [10, "return-values"], [11, "return-values"], [12, "return-values"], [13, "return-values"], [14, "return-values"]], "Status": [[5, "status"], [6, "status"], [7, "status"], [8, "status"], [9, "status"], [10, "status"], [11, "status"], [12, "status"], [13, "status"], [14, "status"], [17, "status"]], "Authors": [[5, "authors"], [6, "authors"], [7, "authors"], [8, "authors"], [9, "authors"], [10, "authors"], [11, "authors"], [12, "authors"], [13, "authors"], [14, "authors"], [17, "authors"]], "hmc_command \u2013 Execute HMC command": [[6, "hmc-command-execute-hmc-command"]], "hmc_pwdpolicy \u2013 Manages the list, create, change and remove password policies of the HMC": [[7, "hmc-pwdpolicy-manages-the-list-create-change-and-remove-password-policies-of-the-hmc"]], "hmc_update_upgrade \u2013 Manages the update and upgrade of the HMC": [[8, "hmc-update-upgrade-manages-the-update-and-upgrade-of-the-hmc"]], "Requirements": [[8, "requirements"], [12, "requirements"], [17, "requirements"], [20, "requirements"]], "Notes": [[8, "notes"], [12, "notes"]], "hmc_user \u2013 Manage the hmc users": [[9, "hmc-user-manage-the-hmc-users"]], "power_system \u2013 PowerOn, PowerOff, modify_syscfg, modify_hwres, facts of the Managed system": [[10, "power-system-poweron-poweroff-modify-syscfg-modify-hwres-facts-of-the-managed-system"]], "powervm_dlpar \u2013 Dynamically managing resources of partition": [[11, "powervm-dlpar-dynamically-managing-resources-of-partition"]], "powervm_lpar_instance \u2013 Create, Delete, Shutdown, Activate, Restart, Facts and Install of PowerVM Partitions": [[12, "powervm-lpar-instance-create-delete-shutdown-activate-restart-facts-and-install-of-powervm-partitions"]], "powervm_lpar_migration \u2013 validate, migrate and recover of the LPAR": [[13, "powervm-lpar-migration-validate-migrate-and-recover-of-the-lpar"]], "vios \u2013 Creation and management of Virtual I/O Server partition": [[14, "vios-creation-and-management-of-virtual-i-o-server-partition"]], "Playbooks": [[15, "playbooks"]], "Playbook Documentation": [[15, "playbook-documentation"]], "Sample Configuration and Setup": [[15, "sample-configuration-and-setup"]], "Inventory": [[15, "inventory"]], "Run the playbooks": [[15, "run-the-playbooks"]], "HMC Password Settings": [[15, "hmc-password-settings"]], "Verbosity": [[15, "verbosity"]], "Plugins": [[16, "plugins"]], "Plugin reference": [[16, "plugin-reference"]], "powervm_inventory \u2013 HMC-based inventory source for Power Servers": [[17, "powervm-inventory-hmc-based-inventory-source-for-power-servers"]], "Quickstart": [[18, "quickstart"]], "ibm.power_hmc": [[18, "ibm-power-hmc"]], "ansible-doc": [[18, "ansible-doc"]], "Connection Method": [[18, "connection-method"]], "Releases": [[19, "releases"]], "Version 1.0.0": [[19, "version-1-0-0"]], "Version 1.1.0": [[19, "version-1-1-0"]], "Version 1.2.0": [[19, "version-1-2-0"]], "Version 1.3.0": [[19, "version-1-3-0"]], "Version 1.4.0": [[19, "version-1-4-0"]], "Version 1.5.0": [[19, "version-1-5-0"]], "Control node": [[20, "control-node"]], "Managed node": [[20, "managed-node"]]}, "indexentries": {}})