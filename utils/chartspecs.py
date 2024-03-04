from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import matplotlib as mpl
import matplotlib.ticker as mtick
import dateutil
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import seaborn as sns
from pathlib import Path
import os
import pandas as pd
import itertools

qtrs = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth'}

current_dir = os.getcwd()
chartbook_dir = Path(os.path.join(current_dir, '..', 'chartbook'))
charts_dir = Path(os.path.join(current_dir, '..', 'charts'))
data_dir = Path(os.path.join(current_dir, '..', 'database'))
notebooks_dir = Path(os.path.join(current_dir, '..', 'notebooks'))
scripts_dir = Path(os.path.join(current_dir, '..', 'scripts'))
utils_dir = Path(os.path.join(current_dir, '..', 'utils'))
text_dir = Path(os.path.join(current_dir, '..', 'texts'))


# Chart Specs
pal = sns.color_palette([
    [0 / 255, 255 / 255, 255 / 255], #Blue
    [255 / 255, 255 / 255, 102 / 255], #Yellow
    [255 / 255, 80 / 255, 80 / 255], #Red
    [255 / 255, 153 / 255, 102 / 255] #Orange
])
# yearsFmt = mdates.DateFormatter('%Y')
# COLOR = 'white'
# mpl.rcParams['text.color'] = COLOR
# mpl.rcParams['axes.labelcolor'] = COLOR
# mpl.rcParams['xtick.color'] = COLOR
# mpl.rcParams['ytick.color'] = COLOR
# mpl.rcParams['lines.color'] = COLOR
# mpl.rcParams['axes.edgecolor'] = COLOR

LEGEND_KWARGS = {'frameon': True, 'framealpha': 0.9, 'labelspacing': 0.4}
# CHART_GAP = timedelta(days=0)
CHART_TITLE_ALIGN = 'left'
# yearsFmt = mdates.DateFormatter('%b-%Y')
# yearsFmt = mdates.DateFormatter('%b-%d')
# yearsFmt = mdates.DateFormatter('%Y')
fontsize = 15
fontweight = 'regular'
title_fontsize = 25
title_fontweight = 'bold'
tick_label_size = 15
tick_label_weight = 'regular'
legend_title_fontsize = 15
legend_title_fontweight = 'regular'
legend_label_fontsize = 15
legend_label_fontweight = 'regular'
annotation_fontsize = 15
annotation_fontweight = 'regular'
xticks_params = {
    # 'pad' : 1,
    'length' : 3,
}
yticks_params = {
    'pad' : 2,
    'length' : 2,
}

savefig_params = {
    'dpi': 72*4,
    'bbox_inches' : 'tight',
    'pad_inches' : 0.4,
}
xlabel_params = {
    # 'position' : (0,0),
    'fontsize' : 15,
    'fontweight' : 'regular',
    # 'labelpad': None,
}
ylabel_params = {
    'fontsize' : 15,
    'fontweight' : 'regular',
}
footnote_params = {
    'xy': (0,-0.17),
    'xycoords':'axes fraction',
    'xytext': (0,-24),
    'textcoords': 'offset points',
    'va': 'top',
    
}
legend_placement_kwargs = {
    'loc': 'upper center',
    'bbox_to_anchor': (.5,-0.10),
    'ncol': 4,
}

grid_kwargs = {
    'linestyle': '-',
    'linewidth': 0.3,
#     'color': 3,
}

footnote_fontsize = 15
footnote_fontweight = 'regular'
fontname = "Baskerville"


def apply_to_axes(axes, footnote_text = 'AllStuffData'):
    _axes = (axes,) if not isinstance(axes, tuple) else axes
    for ax in axes:
        ax.xaxis.label.set_fontsize(xlabel_params['fontsize'])
        ax.yaxis.label.set_fontsize(ylabel_params['fontsize'])
        for item in [ax.xaxis.label, ax.yaxis.label]:
            item.set_fontweight(fontweight)
            item.set_fontname(fontname)
        
        ax.title.set_fontsize(title_fontsize)
        ax.title.set_fontweight(title_fontweight)
        ax.title.set_fontname(fontname)
        
        for item in ax.get_xticklabels() + ax.get_yticklabels():
            item.set_fontsize(tick_label_size)
            item.set_fontweight(tick_label_weight)
            item.set_fontname(fontname)
            
        if ax.get_legend() is not None:
            lt = ax.get_legend().get_title()
            lt.set_fontsize(legend_title_fontsize)
            lt.set_fontweight(legend_title_fontweight)
            lt.set_fontname(fontname)
            for item in ax.get_legend().get_texts():
                item.set_fontsize(legend_label_fontsize)
                item.set_fontweight(legend_label_fontweight)
                item.set_fontname(fontname)

        # footnote = ax.annotate(footnote_text, **footnote_params)
        # footnote.set_fontsize(footnote_fontsize)
        # footnote.set_fontname(fontname)
        # footnote.set_fontweight(footnote_fontweight)
        
    return axes


def write_txt(filename, filetext):
    ''' Write label to txt file '''
    with open(filename, 'w') as text_file:
        text_file.write(filetext)


def dtxt(date):
	'''
	Return strings for given datetime date
	'''
	date = pd.to_datetime(date)
	d = {'qtr1': f'{date.year} Q{date.quarter}', 
	     'qtr2': f'the {qtrs[date.quarter]} quarter of {date.year}',
	     'qtr3': f'Q{date.quarter}',
	     'qtr4': f'`{date.strftime("%y")} Q{date.quarter}',
	     'qtr5': f'the {qtrs[date.quarter]} quarter',
	     'year': f'{date.year}',
	     'mon1': date.strftime('%B %Y'),
	     'mon2': date.strftime('%b %Y'),
	     'mon3': date.strftime('%B'),
	     'mon4': date.strftime(f'`{date.strftime("%y")} {date.strftime("%b")}'),
	     'mon5': date.strftime('%Y-%m'),
	     'mon6': f'{date.strftime("%b")} `{date.strftime("%y")}',
	     'mon7': f'{date.strftime("%b")} {date.strftime("%y")}',
	     'mon8': f'{date.strftime("%b")} \n {date.strftime("%Y")}',
	     'day1': date.strftime('%B %-d, %Y'),
	     'day2': date.strftime('%b %-d, %Y'),
	     'day3': date.strftime('%d'),
	     'day4': date.strftime('%B %-d'),
	     'datetime': date.strftime('%Y-%m-%d'),	
	     'datetime2': date.strftime('%Y-%m-%d').replace('-08-', '-8-').replace('-09-', '-9-')}	
	return d


def value_text(value, style='increase', ptype='percent', adj=None, 
               time_str='', digits=1, threshold=0, num_txt=True,
               casual=False, obj='singular', dollar=False, 
               round_adj=False):
    '''
    RETURN TEXT STRING FOR SPECIFIED FLOAT VALUE
    
    OPTIONS
    style: increase, increase_of, contribution, contribution_to,
           contribution_of, contribution_end
    ptype: percent, pp, None, million, etc
    adj: sa, annual, annualized, saa, saar, total, average
    time_str: blank unless specified directly, for example "one-year"
    num_txt: replace round numbers with text, for example: 9.0 -> nine
    casual: replaces certain words: decreased -> fell, for example
    obj: switch to "plural" if the object is plural, e.g. prices
    round_adj: adds "nearly" to values below the rounded value
    
    '''
    text = 'Error, options not available'
    dol = '' if dollar == False else '$'
    abv = abs(value)
    val = f'{dol}{abv:,.{digits}f}'
    val2 = f'{dol}{value:,.{digits}f}'
    numbers = {'1.0': 'one', '2.0': 'two', '3.0': 'three', 
               '4.0': 'four', '5.0': 'five', 
               '6.0': 'six', '7.0': 'seven', 
               '8.0': 'eight', '9.0': 'nine',
               '10.0': 'ten'}
    if (num_txt == True) & (val in numbers.keys()):
        val = numbers[val] 
    indef = 'an' if ((val[0] == '8') | (val[0:3] in ['11.', '11,', '18.', '18,'])) else 'a'
    neg = True if value < 0 else False
    insig = True if abv < threshold else False
    plural = 's' if ((abv > 1.045) & (style[-3:] != 'end')) else ''
    ptxtd = {None: '', 'none': '', 'None': '', '': '', 'percent': ' percent', 
             'pp': f' percentage point{plural}', 'point': f' point{plural}',
             'trillion': ' trillion', 'billion': ' billion', 'million': ' million', 
             'thousand': ' thousand', 'units': ' units'}
    ptxt = ptxtd[ptype]
    rnd_adj = ('' if ((round_adj == False) | (abv >= round(abv, digits))) 
    		   else 'nearly ' if casual == False else 'almost ')
    
    if style in ['increase', 'increase_by', 'gain', 'return']:
        atxtd = {None: ' by ', 'sa': ' at a seasonally-adjusted rate of ', 
                 'annual': ' at an annual rate of ', 
                 'annualized': ' at an annualized rate of ', 
                 'average_annualized': ' at an average annualized rate of ',
                 'avg_ann': ' at an average annualized rate of ',
                 'saa': ' at a seasonally-adjusted and annualized rate of ', 
                 'saar': ' at a seasonally-adjusted annualized rate of ', 
                 'total': ' by a total of ', 
                 'inflation': ' the inflation rate by ',
                 'average': ' at an average rate of ',
                 'equivalent': ' by the equivalent of '}
        if style != 'increase_by':
            atxtd[None] = ' '
        if style in ['gain', 'return']:
        	atxtd['total'] = ' a total of '
        atxt = atxtd[adj]
        stxt = 'increased' if neg == False else 'decreased'
        if style == 'gain':
        	stxt = 'gained' if neg == False else 'lost'
        if style == 'return':
        	stxt = 'returned' if neg == False else 'lost'
        if adj == 'inflation':
        	stxt = 'increased' if neg == False else 'reduced'
        ttxt = f' over the {time_str} period' if time_str != '' else ''
        text = f'{stxt}{atxt}{val}{ptxt}{ttxt}'
        if insig == True:
            text = 'was virtually unchanged'
            if obj == 'plural':
                text = 'were unchanged'
            
    if style in ['contribution', 'contribution_to']:
        atxtd = {None: '', 'sa': ' on a seasonally-adjusted basis', 
                 'annual': ' on an annual basis', 
                 'annualized': ' on an annualized-basis', 
                 'average_annualized': ' on an average annualized basis ',
                 'avg_ann': ' on an average and annualized rate basis ',
                 'saa': ' on a seasonally-adjusted and annualized basis', 
                 'saar': ' on a seasonally-adjusted annualized basis', 
                 'total': ' in total',
                 'average': ' on an average basis'}
        atxt = atxtd[adj]
        atxt2 = 'the equivalent of ' if adj == 'equivalent' else ''
        stxt = ('contributed', 'to') if neg == False else ('subtracted', 'from')
        ttxt = f' over the {time_str} period' if time_str != '' else ''
        text = f'{stxt[0]} {atxt2}{val}{ptxt}{atxt}{ttxt}'
        if style == 'contribution_to':
            text = f'{stxt[0]} {atxt2}{val}{ptxt} {stxt[1]}'
        if insig == True:
            text = 'did not contribute'
            if style == 'contribution_to':
                text = 'did not contribute to'
            
    elif style in ['increase_of', 'contribution_of', 'return_of']:
        stxt1 = 'increase' if neg == False else 'decrease'
        stxt2 = 'an increase' if neg == False else 'a decrease'
        if style == 'contribution_of':
            stxt1 = 'contribution' if neg == False else 'subtraction'
            stxt2 = 'a contribution' if neg == False else 'a subtraction'    
        if style == 'return_of':
            stxt1 = 'return' if neg == False else 'loss'
            stxt2 = 'a return' if neg == False else 'a loss'   
        if style == 'gain_of':
            stxt1 = 'gain' if neg == False else 'loss'
            stxt2 = 'a gain' if neg == False else 'a loss'             
        if time_str != '':
            stxt2 = f'a {time_str}{stxt1}'
        atxtd = {None: f'{stxt2} of', 'sa': f'a seasonally-adjusted {time_str}{stxt1} of', 
                 'annual': f'an annual {time_str}{stxt1} of', 
                 'annualized': f'an annualized {time_str}{stxt1} of', 
                 'average_annualized': f' an average annualized {time_str}{stxt1} of',
                 'avg_ann': f' an average annualized {time_str}{stxt1} of',
                 'saa': f'a seasonally-adjusted and annualized {time_str}{stxt1} of', 
                 'saar': f'a seasonally-adjusted annualized {time_str}{stxt1} of', 
                 'total': f'a total {time_str}{stxt1} of',
                 'average': f'an average {time_str}{stxt1} of'}
        atxt = atxtd[adj]
        atxt2 = 'the equivalent of ' if adj == 'equivalent' else ''
        text = f'{atxt} {atxt2}{val}{ptxt}'
        if insig == True:
            text = 'virtually no change'
            if style[:3] == 'con':
                text = 'virtually no contribution'
            
    elif style in ['increase_end', 'contribution_end']:
        stxt = 'increase' if neg == False else 'decrease'
        if style == 'contribution_end':
            stxt = 'contribution' if neg == False else 'subtraction'
        atxtd = {None: f'{indef} ', 'sa': 'a seasonally-adjusted ', 
                 'annual': 'an annual ', 
                 'annualized': 'an annualized ', 
                 'average_annualized': ' an average annualized ',
                 'avg_ann': ' an average and annualized ',
                 'saa': 'a seasonally-adjusted and annualized ', 
                 'saar': 'a seasonally-adjusted annualized ', 
                 'total': 'a total ',
                 'average': 'an average '}
        atxt = atxtd[adj]
        ttxt = f'{time_str} ' if time_str != '' else ''
        text = f'{atxt}{ttxt}{val}{ptxt} {stxt}'
        if insig == True:
            text = 'virtually no change'
            if style[:3] == 'con':
                text = 'virtually no contribution'
                
    elif style == 'above_below':
        stxt = 'above' if neg == False else 'below'
        text = f'{val}{ptxt} {stxt}'
        if insig == True:
            text = 'in line with'
            
    elif style == 'plain':
    	val3 = val
    	pn = '' if neg == False else 'negative '
    	# Handle rounded values
    	num_abv = {k[0]: v for k, v in numbers.items()}
    	if (num_txt == True) & (val in num_abv.keys()):
        	val3 = num_abv[val] 
        	if float(val) > value:
        		rnd_adj = 'nearly ' if casual == False else 'almost '
    	text = f'{rnd_adj}{pn}{val3}{ptxt}'
    
    elif style in ['equivalent', 'eq']:
    	atxt = ' of GDP' if adj in ['gdp', 'GDP'] else ''
    	text = f'equivalent to {val}{ptxt}{atxt}'
    	
    elif style == 'added_lost':
    	stxt = 'added' if neg == False else 'lost'
    	atxtd = {None: '', 'average': 'an average of '}
    	atxt = atxtd[adj]
    	text = f'{stxt} {atxt}{val}{ptxt}'
    	
    elif style == 'added_lost_rev':
    	stxt = 'added' if neg == False else 'lost'
    	text = f'{val}{ptxt} {stxt}'
    
    if casual == True:
        text = (text.replace('added', 'gained')
        		    .replace('decreased', 'fell')
                    .replace('contributed', 'added')
                    .replace('increased', 'grew')
                    .replace('contribute ', 'add ')
                    .replace('subtract ', 'remove ')
                    .replace('a contribution', 'an addition')
                    .replace('contribution', 'addition')
                    .replace('decrease', 'fall')
                    .replace('subtraction', 'reduction')
                    .replace('an increase of', 'growth of')
                    .replace('increase of', 'growth of')
                    .replace('decrease of', 'fall of'))
                    
    if obj == 'plural':
        text = (text.replace('was', 'were'))
    
    return(text)


def compare_text(latest, previous, cutoffs, plain=False):
    '''
    Simple text based on difference between two numbers.
    Cutoffs should be list of three numbers that provide scale for 
    how significant the difference is. 
    '''
    direction = 'above' if latest - previous > 0 else 'below'
    size = abs(latest - previous)
    if type(cutoffs) not in [list, tuple] or len(cutoffs) != 3:
        print('Cutoffs should be list of three numeric values')
        
    if size <= cutoffs[0]:
        text = 'in line with'
    elif size <= cutoffs[1]:
        text = f'slightly {direction}'
    elif size <= cutoffs[2]:
        text = f'substantially {direction}'
    else:
        text = f'far {direction}'
    
    if plain == True:
        text = direction
        
    return text