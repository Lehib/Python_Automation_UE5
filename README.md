# Python_Automation
 A repo of python scripts for game dev by Lehi Briscoe

 **automation_menu.py**
 
   Place the scripts in a Python folder in your Content directory in Unreal, then navigate to your project settings, scroll all the way to the bottom of the left menu and select Python, one of the top options will be labelled startup scripts, add a new array element and type in "automation_menu.py". Now as long as the scripts are all in your Content Browser when you restart your project you will have a new menu option called Automation with the scripts below embedded.

   **Set Prefix**
        This script will assess whether your assets have the correct prefix and is designed for clarity and organisation, and if not it will dynamically set them. Currently it will work for textures, materials, material instances, blueprints and has a special process for post process materials.

   **Fix Texture Compression**
        This will analyse the textures within the Content Browser and determine whether they're using the optimal texture compression settings, it is based on the suffixes found at https://gist.github.com/excalith/366e15b13c1c99539aa2600ff3d5e647#textures but has been extended to include ORD maps (Occlusion, Roughness, Displacement).

All functionality may potentially be extended over time, if you encounter any bugs or strange behaviour or just have feedback on the scripts please feel free to get in touch! 

Contact: https://www.linkedin.com/in/lehi-briscoe/
