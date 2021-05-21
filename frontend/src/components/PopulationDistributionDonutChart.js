import React from 'react'
import ReactApexChart from 'react-apexcharts';
import './PopulationDistributionDonutChart.css'

class PopulationDistributionDonutChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        series: [44, 55, 41, 17, 15],
        options: {
          chart: {
            type: 'donut',
          },
          labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }],
          plotOptions: {
            pie: {
              donut: {
                labels: {
                  show: true,
                  total: {
                    showAlways: true,
                    show: true
                  }
                }
              }
            }
          },
      }
    }
    }

    render() {
      return (
        <div className="donut">
            <div className="title">{this.props.name}</div>
            <ReactApexChart options={this.state.options} series={this.state.series} type="donut" />
        </div>
      );
    }
  }
export default PopulationDistributionDonutChart;