import os
import requests
import pandas as pd

def download_uci_online_retail(destination_folder="sample-datasets"):
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    filename = "uci-online-retail.xlsx"
    os.makedirs(destination_folder, exist_ok=True)
    dest_path = os.path.join(destination_folder, filename)

    print(f"Downloading UCI Online Retail dataset to {dest_path}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(dest_path, "wb") as f:
        f.write(response.content)
    print("Download complete.")

def convert_excel_to_csv(excel_path, csv_path):
    df = pd.read_excel(excel_path)
    df.to_csv(csv_path, index=False)
    print(f"Converted {excel_path} to {csv_path}")

PRODUCT_CLASS_KEYWORDS = {
    'Home Decor': [
        'lantern', 'mirror', 'clock', 'candle', 't-light', 'ornament',
        'doormat', 'rug', 'cushion', 'garland', 'wreath', 'sign',
        'frame', 'plant', 'vase', 'platter', 'planter', 'hook', 'cabinet',
        'shelf', 'stand', 'basket'
    ],
    'Kitchenware': [
        'mug', 'cup', 'saucer', 'teaspoon', 'spoon', 'bowl', 'plate',
        'jug', 'coaster', 'napkin', 'cutlery', 'baking', 'cookie cutter',
        'oven glove', 'apron', 'tea cosy', 'teapot', 'kettle'
    ],
    'Toys & Games': [
        'doll', 'toy', 'jigsaw', 'puzzle', 'game', 'marbles', 'ludo',
        'skittles', 'rocket', 'model', 'balloon', 'marble', 'board game'
    ],
    'Stationery & Craft': [
        'notebook', 'journal', 'sketchbook', 'pen', 'pencil', 'eraser',
        'sticker', 'card', 'envelope', 'ribbon', 'tissue', 'wrap',
        'paint', 'marker', 'chalk', 'craft', 'incense', 'stencil', 'bead'
    ],
    'Bags & Luggage': [
        'bag', 'tote', 'backpack', 'luggage', 'passport cover', 'tag',
        'umbrella', 'case', 'purse', 'wallet', 'satchel'
    ],
    'Storage & Organization': [
        'box', 'container', 'organiser', 'organizer', 'rack', 'stand',
        'crate', 'holder', 'tin', 'drawer'
    ],
    'Personal Accessories': [
        'scarf', 'hat', 'glove', 'necklace', 'bracelet', 'earring',
        'ring', 'bangle', 'hair', 'mirror', 'key ring', 'cufflink'
    ],
    'Garden & Outdoor': [
        'garden', 'plant', 'watering can', 'birdcage', 'birdhouse',
        'thermometer', 'bench', 'planter', 'parasol', 'spade', 'rake',
        'trowel', 'hose'
    ],
    'Textiles': [
        'cushion', 'blanket', 'throw', 'towel', 'quilt', 'scarf', 'rug'
    ],
    'Seasonal & Holiday': [
        'christmas', 'easter', 'valentine', 'halloween', 'advent',
        'festive', 'gift', 'stocking'
    ],
}

PRODUCT_SUBCLASS_KEYWORDS = {
    'Lantern': ['lantern'],
    'T-Light Holder': ['t-light', 'tealight', 't light', 't-light holder'],
    'Candle': ['candle', 'votive', 'pillar', 'wick'],
    'Clock': ['clock', 'alarm clock', 'wall clock', 'table clock'],
    'Picture Frame': ['frame', 'photo frame', 'cornice'],
    'Mirror': ['mirror'],
    'Basket': ['basket', 'crate'],
    'Cabinet': ['cabinet', 'drawer', 'shelf'],
    'Jug': ['jug', 'pitcher'],
    'Mug': ['mug', 'cup', 'beaker', 'teacup'],
    'Bowl': ['bowl'],
    'Plate': ['plate', 'platter'],
    'Coaster': ['coaster'],
    'Cutlery Set': ['cutlery'],
    'Teaspoon': ['teaspoon', 'spoon'],
    'Apron': ['apron'],
    'Oven Glove': ['oven glove', 'oven mitt'],
    'Cookie Cutter': ['cookie cutter'],
    'Doll': ['doll'],
    'Soft Toy': ['soft toy', 'toy'],
    'Game': ['game', 'ludo', 'skittles', 'board game'],
    'Puzzle': ['jigsaw', 'puzzle'],
    'Notebook': ['notebook', 'journal', 'sketchbook', 'pad'],
    'Pen/Pencil': ['pen', 'pencil', 'marker'],
    'Sticker': ['sticker'],
    'Card': ['card', 'postcard', 'greeting card'],
    'Gift Wrap': ['wrap', 'gift bag', 'ribbon', 'gift tape'],
    'Doormat': ['doormat'],
    'Sign': ['sign', 'metal sign', 'wall art'],
    'Organiser': ['organiser', 'organizer', 'tidy'],
    'Thermometer': ['thermometer'],
    'Key Ring': ['key ring', 'key fob'],
    'Umbrella': ['umbrella', 'parasol'],
    'Baking Case': ['cake case', 'baking case'],
    'Candle Set': ['set of', 'box of'],
}

def classify_description(description):
    """
    Classify a single product description into
    product_class and product_subclass by keyword lookup.
    """
    desc = str(description).lower() if pd.notnull(description) else ""
    product_class = 'Miscellaneous'
    for cls, keywords in PRODUCT_CLASS_KEYWORDS.items():
        if any(kw in desc for kw in keywords):
            product_class = cls
            break

    product_subclass = 'Other'
    for subcls, keywords in PRODUCT_SUBCLASS_KEYWORDS.items():
        if any(kw in desc for kw in keywords):
            product_subclass = subcls
            break
    return pd.Series([product_class, product_subclass])

def add_product_class_columns(csv_path):
    df = pd.read_csv(csv_path)
    df[["product_class", "product_subclass"]] = df["Description"].apply(classify_description)
    df.to_csv(csv_path, index=False)
    print("Added product_class and product_subclass columns.")

if __name__ == "__main__":
    download_uci_online_retail()
    excel_path = os.path.join("sample-datasets", "uci-online-retail.xlsx")
    csv_path = os.path.join("sample-datasets", "uci-online-retail.csv")
    convert_excel_to_csv(excel_path, csv_path)
    add_product_class_columns(csv_path)
    os.remove(excel_path)