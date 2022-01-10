# Bar chart race for Messenger

You need pandas and bar_chart_race python modules
```
pip install pandas bar_chart_race
```
You also need ffmpeg. You can install it with brew with
```
brew install ffmpeg
```

You can create two different types of bar chart races. One with the total amount of messages of all time:
```
python main.py --days all
```

Furthermore, you can create a "rolling" count of messages. For example, to have a bar chart race that only includes count of the past 180 days, run
```
python main.py --days 180
```