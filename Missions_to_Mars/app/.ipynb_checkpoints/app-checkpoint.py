{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, render_template, redirect\n",
    "import pymongo\n",
    "from flask_pymongo import PyMongo\n",
    "#import scrape_mars\n",
    "#import scrape_mars\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Flask Setup\n",
    "app = Flask(__name__)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "client = pymongo.MongoClient('mongodb://localhost:27017')\n",
    "db = client.mars_db\n",
    "collection = db.mission"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create route that renders index.html template and finds documents from mongo\n",
    "@app.route('/')\n",
    "def index():\n",
    "    mission = collection.find_one()\n",
    "    return render_template('index.html, mission=mission')\n",
    "\n",
    "\n",
    "# Create route that will trigger scrape functions\n",
    "@app.route('/scrape')\n",
    "def scrape():\n",
    "    mission = collection\n",
    "    mission_data = scrape_mars.scrape()\n",
    "    mission.update({}, mission_data, upsert=True)\n",
    "    return 'Scraped'\n",
    "    #db.mission.drop()\n",
    "    \n",
    "if __name__ =='__main__':\n",
    "    app.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
