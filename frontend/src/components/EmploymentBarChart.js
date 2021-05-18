import React from 'react'
import Chart from 'react-apexcharts'

class EmploymentBarChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        series: [],
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
            text: 'Provisional Mortality Statistics 2020'
          },
          noData: {
            text: 'Loading...'
          },
          xaxis: {
            categories: ['2016', '2019', '2020'],
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

    componentDidMount() {
        fetch("http://127.0.0.1:8000/api/employment")
          .then(res => res.json())
          .then(
            (result) => {
              this.setState({
                isLoaded: true,
                series: result.series
              });
            },
            (error) => {
              this.setState({
                isLoaded: true,
                error
              });
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
export default EmploymentBarChart;