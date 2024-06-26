# anixart-to-shikimori

Python script that allows you to extract anime data from Anixart and save it in JSON format for Shikimori

## Install

1. Make sure you have Python installed (version 3.6 or higher is recommended).
2. Clone this repository using the following command:

   ```shell
   git clone https://github.com/the-dise/anixart-to-shikimori.git
   cd anixart-to-shikimori
   ```

3. Install the dependencies using the following command:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

1. Place the **Anixart_Bookmarks.txt** file in the project directory.
2. Convert **Anixart_Bookmarks.txt** to UFT-8. By default it is saved in UTF-8 with BOM.
3. Run the script using the following command:

   ```shell
   python ./main.py
   ```

4. When the script completes, the results will be saved to the anime_data.json file.
5. Go to Shikimori profile settings and import anime_data.json.

## How to export Anixart data

Go to Profile tab -> Settings -> Data Management - Export bookmarks

|                                         1                                         |                                         2                                         |                                         3                                         |
| :-------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------: |
| ![](https://github.com/the-dise/anixart-to-shikimori/blob/main/src/images/00.jpg) | ![](https://github.com/the-dise/anixart-to-shikimori/blob/main/src/images/01.jpg) | ![](https://github.com/the-dise/anixart-to-shikimori/blob/main/src/images/02.jpg) |

## License

This project is licensed under the [MIT](LICENSE) license.
