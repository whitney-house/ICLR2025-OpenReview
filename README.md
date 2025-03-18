# **ICLR 2025 Paper Analysis using OpenReview API**  

This project automatically fetches ICLR 2025 paper submission data using the OpenReview API.It has used Tenacity to avoid rate limit error:)

## **Usage**   
**1.** Sign up for an OpenReview account by following [this guide](https://docs.openreview.net/getting-started/creating-an-openreview-profile/signing-up-for-openreview).  
**2.** Clone this repository:  
   ```bash
   git clone https://github.com/whitney-house/ICLR2025-OpenReview/tree/main
   cd ICLR2025-OpenReview
   ```
**3.** Set up an conda environment (Recommended)
   ```bash
   conda create -n <your environment name>
   conda activate <your environment name>
   ```  
   
**4.** Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```
   
**5.** Store your OpenReview credentials as environment variables in Conda:
   ```bash
   conda env config vars set OPENREVIEW_USERNAME=<your_username>
   conda env config vars set OPENREVIEW_PASSWORD=<your_password>
   conda activate <your_environment_name>
   ```
   
**6.** If you prefer using a .env file instead of Conda environment variables, create a .env file **(Don't upload to github)** in the project root and add:
   ```bash
   OPENREVIEW_USERNAME=<your_username>
   OPENREVIEW_PASSWORD=<your_password>
   ```
   Then install python-dotenv (if not already installed):
   ```bash
   pip install python-dotenv
   ```
   Then in **fetch_data.py** write like this:
   ```bash
   from dotenv import load_dotenv
   import os

   load_dotenv()  
   USERNAME = os.getenv("OPENREVIEW_USERNAME")
   PASSWORD = os.getenv("OPENREVIEW_PASSWORD")
   ```  

**7.** run the scripts: 
   ```bash
   python3 main.py
   ```

**8.** Sit back, relax, and enjoy the results! 🎉

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** License.  

You are free to:
- **Share** — Copy and redistribute the material in any medium or format.
- **Adapt** — Remix, transform, and build upon the material.

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial** — You may not use the material for commercial purposes.

For more details, see the **[LICENSE](LICENSE)** file or visit the full license text:  
🔗 [CC BY-NC 4.0 License](https://creativecommons.org/licenses/by-nc/4.0/)


