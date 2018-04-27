import plotly
from plotly import tools
import plotly.graph_objs as go
import numpy as np
from matplotlib.pyplot import cm


class PlotCreator:

    def __init__(self, plot_type: str, n_plots: int):
        """
        """
        self.__color = [tuple(i[:3]*252) for i in cm.jet(np.linspace(0, 1, n_plots))]

        self.plot_type = plot_type
        if plot_type == 'scatter':
            self.scatter_data = []
        elif plot_type == 'lines':
            self.lines_data = []
        elif plot_type == 'bar':
            self.bar_data = []

    def add_timeseries_to_plot(self, x, y, idx: int, dash=None,
                               label_string=None, fill_to_zero=False, hover_info=None,
                               color=None):
        """
            Add scatter to plot
        :param x
            forecast:
            list, np.array or pd.series of normalized forecast
        :param y
            measurement:
            list, np.array or pd.series of normalized measurement
        :param color:
        :return:
        """
        data = dict(x=x,
                    y=y,
                    mode='lines')

        if label_string is not None:
            data.update(dict(name=label_string))
        else:
            data.update(dict(showlegend=False))

        if hover_info is not None:
            data.update(dict(hoverinfo="y+text",
                             hovertext=hover_info))
        if color is not None:
            data.update(dict(line=dict(color=('rgb' + str(color)))))
        else:
            data.update(dict(line=dict(color=('rgb' + str(self.__color[idx])))))

        if fill_to_zero:
            data.update(dict(fill='tozeroy'))
        if dash:
            data['line'].update(dict(dash=dash))

        self.lines_data.append(go.Scatter(data))

    def add_scatter(self, x, y, label_string=''):
        """
            Add scatter to plot
        :param x
            forecast:
            list, np.array or pd.series of normalized forecast
        :param y
            measurement:
            list, np.array or pd.series of normalized measurement
        :param color:
        :return:
        """
        self.scatter_data.append(go.Scatter(
            x=x,
            y=y,
            mode='markers',
            name=label_string))

    def proceed_scatter_plot(self, file_name: str, title: str, xlab: str, ylab: str):
        self.scatter_data.append(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            line=dict(
                color=('rgb(0, 0, 0)'))))
        layout = dict(
            title=title,
            paper_bgcolor='rgb(255,255,255)',
            plot_bgcolor='rgb(229,229,229)',
            xaxis=dict(
                title=xlab,
                gridcolor='rgb(255,255,255)',
                range=[0, 1],
                showgrid=True,
                showline=False,
                showticklabels=True,
                tickcolor='rgb(127,127,127)',
                ticks='outside',
                zeroline=False
            ),
            yaxis=dict(
                title=ylab,
                gridcolor='rgb(255,255,255)',
                range=[0, 1],
                showgrid=True,
                showline=False,
                showticklabels=True,
                tickcolor='rgb(127,127,127)',
                ticks='outside',
                zeroline=False
            ),
        )
        fig = dict(data=self.scatter_data, layout=layout)
        plotly.offline.plot(fig, filename=file_name+'.html', auto_open=False)

    def scattergeo(self, lon_data: np.ndarray, lat_data: np.ndarray,
                   lon_bounds: list, lat_bounds: list, title: str,  f_name: str,
                   plot_data=None, text=None, size=3, colorbar=True, zbounds=None, label=None):
        data = [dict(
            type=self.plot_type,
            lon=lon_data,
            lat=lat_data,
            mode='markers',
            # symbol = 'square'
        )]
        layout = dict(
            title=title,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                showland=True,
                showocean=True,
                showcountries=True,
                showsubunits=True,
                projection=dict(
                    type='Mercator'
                ),
                scope='europe',
                lonaxis=dict(range=lon_bounds),
                lataxis=dict(range=lat_bounds),
                resolution='50',
                showrivers=True,
                showlakes=True
            )
        )
        if text is not None:
            data[0].update(dict(text=text))
        if plot_data is not None:
            data[0].update(dict(marker=dict(
                color=data,
                size=size,
                opacity=1,
                reversescale=False,
                autocolorscale=False,
                )))
        if colorbar:
            data[0].update(
                marker=dict(
                colorbar=dict(
                thickness=10,
                titleside="right",
                ticks="outside",
                ticksuffix=label)
            ))

        fig = dict(data=data, layout=layout)
        plotly.offline.plot(fig, filename=f_name+'.html', auto_open=False)

    def add_bar(self, x, y, idx: int, label_string=None, color=None):
        data = dict(x=x,
                    y=y,
                    mode='bar',
                    name=label_string)

        if color is not None:
            data.update(dict(line=dict(color=('rgb' + str(color)))))
        else:
            data.update(dict(line=dict(color=('rgb' + str(self.__color[idx])))))


        self.bar_data.append(go.Bar(data))

    def proceed_bar_plot(self, file_name: str, title: str, ylab: str, xrange=None, yrange=[0, 1]):
        layout = go.Layout(
            title=title,
            yaxis=dict(
                title=ylab,
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode='group',
            bargap=0.05,
            bargroupgap=0.1
        )

        fig = go.Figure(data=self.bar_data, layout=layout)
        plotly.offline.plot(fig, filename=file_name+'.html', auto_open=False)

    def proceed_timeseries_plot(self, file_name: str, title: str, ylab: str, xrange=None, yrange=[0, 1], rangeslider=False,
                                linewidth=4, theme='dark'):

        if theme == 'white':
            color1 = 'rgb(127,127,127)'
            color2 = 'rgb(255,255,255)'
            color3 = 'rgb(229,229,229)'
            color4 = 'rgb(255,255,255)'
            color5 = '#5b5b5b'
        elif theme == 'dark':
            color1 = 'rgb(255,255,255)'
            color2 = '#333333'
            color3 = '#5b5b5b'
            color4 = 'rgb(193,193,193)'
            color5 = '#5b5b5b'

        layout = dict(
            title=title,
            paper_bgcolor=color2,
            plot_bgcolor=color3,
            font=dict(color= color1),
            xaxis=dict(
                gridcolor=color4,
                showgrid=True,
                showline=False,
                showticklabels=True,
                tickcolor=color1,
                tickfont=dict(color=color1),
                ticks='outside',
                zeroline=False,
                linewidth=linewidth,
            ),
            yaxis=dict(
                title=ylab,
                gridcolor=color4,
                range=yrange,
                showgrid=True,
                showline=False,
                showticklabels=True,
                tickcolor=color1,
                tickfont=dict(color=color1),
                ticks='outside',
                zeroline=False,
            ),
            legend=dict(
                x=0.05,
                y=1,
                traceorder='normal',
                font=dict(
                    family='sans-serif',
                    size=20,
                    color=color1
                ),
                bgcolor=color5,
                bordercolor=color1,
                borderwidth=2
            ),
            margin=go.Margin(
            l=50,
            r=10,
            b=40,
            t=30
            )
        )
        if rangeslider:
            layout['xaxis'].update(dict(rangeselector=dict(
                buttons=list([
                        dict(count=1,
                             label='1d',
                             step='day',
                             stepmode='backward'),
                        dict(count=30,
                             label='30d',
                             step='month',
                             stepmode='backward')])
                ),
                rangeslider=dict(),
                type='date'))

        if xrange != None:
            layout['xaxis'].update(range=xrange)

        fig = dict(data=self.lines_data, layout=layout)

        return plotly.offline.plot(fig, filename=file_name+'.html', auto_open=False)

    # def add_statistics_box(self, stat_value, label, idx, einheit, idx_color, colour=None):
    #     x_offset = min(plt.xlim())
    #     size = max(plt.xlim()) - min(plt.xlim())
    #     y_offset = max(plt.ylim())
    #     if colour != None:
    #         plt.text(x_offset + 0.02 * size, (y_offset * 0.96 - idx * 0.05), label + str(stat_value) + einheit,
    #                  bbox={'facecolor': colour, 'alpha': 0.1, 'pad': 2}, )
    #     else:
    #         plt.text(x_offset + 0.02 * size, (y_offset * 0.96 - idx * 0.05), label + str(stat_value) + einheit,
    #                  bbox={'facecolor': self.__color[idx_color], 'alpha': 0.1, 'pad': 2}, )
    #
    # def proceed_plot(self, title, file_name, ylab, ylim=(0, 1), legend=True, second_y_axis=None):
    #     hfmt = DateFormatter('%Y-%m-%d %H:%M')
    #     plt.style.use('ggplot')
    #     plt.title(title)
    #     plt.grid(True)
    #     plt.tick_params(axis='both', which='major', labelsize=12)
    #     self.__ax.xaxis.set_major_formatter(hfmt)
    #     self.__ax.set_ylim(ylim)
    #     self.__ax.set_ylabel(ylab, fontsize=15)
    #     if second_y_axis is not None:
    #         ax2 = self.__ax.twinx()
    #         ax2.set_ylim(second_y_axis)
    #         self.__align_axis(ax2)
    #         ax2.set_ylabel('total Power [GW]', fontsize=15)
    #         ax2.tick_params(axis='both', which='major', labelsize=12)
    #     if legend:
    #         plt.legend(fancybox=True, fontsize='small')
    #     self.__fig.autofmt_xdate()
    #     plt.savefig(file_name + '.png', bbox_inches='tight')
    #     plt.clf()
    #
    # def proceed_series_plot(self, title, file_name, ylab):
    #     plt.legend(fancybox=True, fontsize='small')
    #     plt.ylim(0, 1)
    #     plt.ylabel(ylab)
    #     plt.title(title)
    #     plt.grid(True)
    #     plt.style.use('bmh')
    #     plt.savefig(file_name + '.png', bbox_inches='tight')
    #     plt.clf()
    #
    # def __align_axis(self, ax2):
    #     """
    #         Sets both axes to have the same number of gridlines
    #         ax1: left axis
    #         ax2: right axis
    #         step: defaults to 1 and is used in generating a range of values to check new boundary
    #               as in np.arange([start,] stop[, step])
    #
    #     """
    #     self.__ax.set_aspect('auto')
    #     ax2.set_aspect('auto')
    #     grid_l = len(self.__ax.get_ygridlines())  # N of gridlines for left axis
    #     #  Choose the axis with smaller N of gridlines
    #     y_min_r, y_max_r = ax2.get_ybound()
    #     y_min_l, y_max_l = self.__ax.get_ybound()
    #     parts = (y_max_l - y_min_l) / (grid_l - 1)
    #     y_new = np.arange(0, y_max_r, y_max_r*parts)
    #     ax2.set_yticks(y_new.round(1))
