import unreal

from set_prefix import SetPrefix
from fix_texture_compression import FixTextureCompression


def create_automation_menu(menu):
    return menu.add_sub_menu(
        owner=unreal.Name("PythonAutomation"),
        section_name=unreal.Name(""),
        name=unreal.Name("PythonAutomation"),
        label=unreal.Text("Automation"),
        tool_tip=unreal.Text("Python automation scripts"),
    )


def setup_prefix_script(section_name) -> SetPrefix:
    prefix_script_object = SetPrefix()

    prefix_script_object.init_entry(
        owner_name=unreal.Name("PythonAutomation"),
        menu=unreal.Name("LevelEditor.MainMenu.PythonAutomation"),
        section=general_section_name,
        name=unreal.Name("SetPrefix"),
        label=unreal.Text("Set Prefixes"),
        tool_tip=unreal.Text("Set the prefixes for assets in the Content Browser"),
    )

    prefix_script_object.register_menu_entry()

    # icon
    prefix_script_data = prefix_script_object.data
    prefix_script_icon = unreal.ScriptSlateIcon(
        style_name=unreal.Name("Palette.Icon"),
        small_style_name=unreal.Name("Palette.Icon.Small"),
        style_set_name=unreal.Name("UMGStyle"),
    )
    prefix_script_data.icon = prefix_script_icon

    return prefix_script_object


def setup_compression_script(section_name) -> FixTextureCompression:
    compression_script_object = FixTextureCompression()

    compression_script_object.init_entry(
        owner_name=unreal.Name("PythonAutomation"),
        menu=unreal.Name("LevelEditor.MainMenu.PythonAutomation"),
        section=general_section_name,
        name=unreal.Name("FixCompression"),
        label=unreal.Text("Fix Texture Compression"),
        tool_tip=unreal.Text(
            "Set the texture compression settings for textures in the Content Browser"
        ),
    )

    compression_script_object.register_menu_entry()

    # icon
    compression_script_data = compression_script_object.data
    compression_script_icon = unreal.ScriptSlateIcon(
        style_name=unreal.Name("Palette.Icon"),
        small_style_name=unreal.Name("Palette.Icon.Small"),
        style_set_name=unreal.Name("UMGStyle"),
    )
    compression_script_data.icon = compression_script_icon

    return compression_script_object

if __name__ == "__main__":
    tool_menus = unreal.ToolMenus.get()
    main_menu = tool_menus.find_menu(unreal.Name("LevelEditor.MainMenu"))

    automation_menu = create_automation_menu(menu=main_menu)

    general_section_name = unreal.Name("GeneralAutomation")
    automation_menu.add_section(general_section_name, unreal.Text("General"))

    # next steps: adding GUI to give users option of adding or removing EXISTING_PREFIXES and EXCLUSIONS
    # gather a larger list for PREFIX_MAPPING, and maybe see if it's possible to give users access to change the values

    # Create an instance of SetPrefix
    prefix_script_object = setup_prefix_script(general_section_name)
    compression_script_object = setup_compression_script(general_section_name)

    # Refresh menu to update changes
    tool_menus.refresh_all_widgets()
