import plotnine as p9
import pandas as pd
import matplotlib.pyplot as plt

def construct_balance_sheet(assets: dict, liabilities: dict) -> pd.DataFrame:
    
    balance_sheet_side   = ['Assets'] * len(assets) + ['Liabilities'] * len(liabilities) 
    balance_sheet_items = list(assets.keys()) + list(liabilities.keys())
    balance_sheet_items  = pd.Categorical(balance_sheet_items, categories=balance_sheet_items)
    balance_sheet_values = list(assets.values()) + list(liabilities.values())
                                                                                  
    balance_sheet = pd.DataFrame(
        {'Side': balance_sheet_side,
         'Item': balance_sheet_items, 
         'Value': balance_sheet_values,
        }
    )
        
    return balance_sheet
    
    
def plot_balance_sheet(balance_sheet: pd.DataFrame, display_amounts: bool =True, unit: str ='mUSD'):

    # X-axis lables (Assets / Liabilities) on top:
    plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.labeltop'] = True
    plt.rcParams['xtick.top'] = False
    
    if display_amounts:
        balance_sheet.Item = balance_sheet.Item.str.cat(balance_sheet.Value.astype(str), ", " ) + unit

    balance_sheet.Item = pd.Categorical(balance_sheet.Item,  categories=balance_sheet.Item, ordered=True)
    # balance_sheet['Item'] = balance_sheet.Item.astype('category')
    
    balance_sheet_plot = (
        p9.ggplot(balance_sheet, p9.aes(x='Side', y='Value', fill='factor(Item)')) 

        + p9.geom_bar(stat='identity', position='stack')  # show_legend=False 
        # + p9.geom_col(stat='identity')
        
        + p9.geom_text(p9.aes(label='Item'), position=p9.position_stack(vjust=0.5))  # , position='Value
        + p9.xlab('')
        + p9.ylab('')    
        + p9.themes.theme_void()
        + p9.theme(
            legend_position='none',
            text=p9.element_text(size=16), 
            axis_text_y = p9.element_blank(), 
            axis_ticks_major = p9.element_blank(),
        )
        + p9.scale_fill_brewer(type="seq", palette="Blues", direction=1)
        + p9.scale_x_discrete(limits=['Assets', 'Liabilities'])  # , position = "top"
    )
    
    # TODO:
    # - use different color scales for Assets and Liabilities 

    # fig  = bs_plot.draw(show=True)
    # axes = fig.get_axes()
    # axes[0].xaxis.tick_top()
    # axes[0].xaxis.set_label_position('top')

    return balance_sheet_plot