import React from 'react'
import Chart from 'react-apexcharts'

class LanguageDistributionBarChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        series: [{
            data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380],
        }],
        options: {
          chart: {
            type: 'bar',
            height: 500,
          },
          plotOptions: {
            bar: {
              horizontal: true,
            },
          },
          stroke: {
            width: 1,
            colors: ['#fff']
          },
          title: {
            text: ''
          },
          noData: {
            text: 'Loading...'
          },
          xaxis: {
            categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
            'United States', 'China', 'Germany'],
          },
          yaxis: {
            title: {
              text: undefined
            },
          },
          fill: {
            opacity: 1
          },
          legend: {
            position: 'top',
            horizontalAlign: 'left',
            offsetX: 40
          }
        },
      
      
      };
    }

    componentDidMount(){
        console.log(this.props)
        this.setState({
        })
    }

    render() {
      return (
        <div className="app">
        <div className="row">
          <div className="mixed-chart">
            <Chart
              options={this.state.options}
              series={this.state.series}
              type="bar"
              width="800"
            />
          </div>
        </div>
      </div>
      );
    }
  }
export default LanguageDistributionBarChart;