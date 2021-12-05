{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "app.py",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyO7lnp5e1l2tfDbFcYc1iep"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "metadata": {
        "id": "clyKPzpEEwey"
      },
      "source": [
        "from flask import Flask, render_template, jsonify, request\n",
        "app = Flask(__name__)\n",
        "\n",
        "from pymongo import MongoClient\n",
        "client = MongoClient('localhost', 27017)\n",
        "db = client.dbsparta\n",
        "\n",
        "## HTML을 주는 부분\n",
        "@app.route('/')\n",
        "def home():\n",
        "    return render_template('index.html')\n",
        "\n",
        "## API\n",
        "@app.route('/moviedetails', methods=['GET'])\n",
        "def moviedetails():\n",
        "    moviedetails = list(db.MovieDetails.find({},{'_id':False}))\n",
        "    return jsonify({\"all_details\": moviedetails})\n",
        "\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    app.run('0.0.0.0', port=5001, debug=True)"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}