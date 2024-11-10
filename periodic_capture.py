import unreal

# spawn a camera actor


# access camera actors viewport


# Unreal function for taking a screen grab of that cameras viewport


# find out if there’s a way to implement logic that takes those screen captures automatically upon file save
# have an option for the user to change how many captures are taken based on whether it’s a longer or shorter sequence
# give the script user the freedom to choose what the name is saved as and where
# make the script automatically increment the saves name upon choosing a longer sequence if it doesn’t by default
# maybe have the script save each sequence in its own numbered directory if it’s taking more than one snap so that  it doesn’t muddle up the versions, or if not have the increment feature also add a prefix that identifies them
# it may be good to do it on autosave as an option too but if you want it to work best maybe it should be on playing the effect otherwise you won’t see anything, so whatever the button is to begin playing the effect should trigger the function, maybe with a buffer so that it won’t activate more than once a minute to avoid going overboard

custom_menu = asset_context_menu.add_sub_menu(
    "", # context
    "", # section
    "", # name
    "", # label
)

separator_entry = unreal.ToolMenuEntry(name=unreal.Name("separator entry"), type=unreal.MultiBlockType.SEPARATOR)
custom_menu.add_menu_entry("", separator_entry)