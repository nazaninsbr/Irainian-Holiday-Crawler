# Irainian-Holiday-Crawler

You can download the`holiday_crawler.py` file, place it next to your code and use it like this:

```python
from holiday_crawler import HolidayCrawler

start_year = 2010
end_year = 2020

hc = HolidayCrawler(start_year, end_year)
hc.run()
```

The code downloads two different versions of holidays. 

The first version (_v1) is crawled from the following website:

https://www.timeanddate.com/holidays/iran/

and the second version (_v2) from this website:

https://calendarific.com/holidays/2019/IR

The second version includes days of the week as well as dates. The first file, however, includes a couple of more dates in each year. 

You can use whichever feels more credible to you. 

### Don't Use The Notebook

The Jupyter Notebook is the dirty version of the code and is basically what I used to figure out how to get the date. If you want to use this I would not suggest using the notebook. You could however use it to see the output formats and ... .
