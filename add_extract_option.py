import winreg
import getpass


def run(exe_path, icon_path):
    icon_path = f'"{icon_path}"'
    username = getpass.getuser()
    print("Windows Username:", username)

    # Create the parent key for the shell extension for ZIP files

    zip_key_path = r"CompressedFolder\Shell\zipHelper"
    zip_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, zip_key_path)
    winreg.SetValue(zip_key, "", winreg.REG_SZ, "Extração xibística com zipHelper")
    winreg.CloseKey(zip_key)

    # Create the key for the shell extension's command for ZIP files
    zip_command_path = r"CompressedFolder\Shell\zipHelper\command"
    zip_command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, zip_command_path)
    winreg.SetValue(zip_command_key, "", winreg.REG_SZ, f'{exe_path} "%1"')
    winreg.CloseKey(zip_command_key)

    # Create a subkey to specify the icon for ZIP files
    zip_icon_path = r"CompressedFolder\Shell\zipHelper"
    rar_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, zip_icon_path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(rar_key, "Icon", 0, winreg.REG_SZ, icon_path)

    # Create the parent key for the shell extension for RAR files
    rar_key_path = r"WinRAR\Shell\zipHelper"
    rar_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rar_key_path)
    winreg.SetValue(rar_key, "", winreg.REG_SZ, "Extração xibística com zipHelper")
    winreg.CloseKey(rar_key)

    # Create the key for the shell extension's command for RAR files
    rar_command_path = r"WinRAR\Shell\zipHelper\command"
    rar_command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rar_command_path)
    winreg.SetValue(rar_command_key, "", winreg.REG_SZ, f'{exe_path} "%1"')
    winreg.CloseKey(rar_command_key)

    # Create a subkey to specify the icon for RAR files
    rar_icon_path = r"WinRAR\Shell\zipHelper"
    rar_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, rar_icon_path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(rar_key, "Icon", 0, winreg.REG_SZ, icon_path)
