import React from 'react'
import Chart from 'react-apexcharts'

class DeathBarChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
      
        series: [{
          name: 'Covid-19',
          data: [0, 0, 21, 63, 9,2,133,445,139,15,4,1]
        }, {
          name: 'Respiratory diseases',
          data: [1026, 949, 1107, 1009, 1027, 987,1020,1048,1050,918,906,996]
        }, {
          name: 'Influenza and pneumonia',
          data: [179, 183,237,232,189,186,192,186,153,129,124,145]
        }, {
          name: 'Chronic lower respiratory conditions',
          data: [569,538,605,526,550,547,537,570,605,550,522,577]
        }, {
          name: 'Cancer',
          data: [3964,3857,4044,3861,4113,3826,4176,3996,3946,4070,3992,4122]
        },{
            name: 'Ischaemic heart diseases',
            data: [1017,998,1069,1105,1221,1138,1204,1279,1204,1132,1038,1079]
        },{
            name: 'Cerebrovascular diseases',
            data: [685,660,707,776,844,789,769,816,748,782,709,704]
        },{
            name: 'Dementia including Alzheimers',
            data: [1157,1124,1247,1285,1240,1188,1272,1294,1200,1197,1119,1178]
        },{
            name: 'Diabetes',
            data: [334,374,392,456,415,417,428,435,422,420,378,408]
        }],
        options: {
          chart: {
            type: 'bar',
            height: 500,
            stacked: true,
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
          xaxis: {
            categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
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
        fetch("http://127.0.0.1:8000/api/death/all")
          .then(res => res.json())
          .then(
            (result) => {
                console.log(result.Cancer)
              this.setState({
                isLoaded: true,
                seriesValue: result
              });
            },
            (error) => {
              this.setState({
                isLoaded: true,
                error
              });
            } )
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
export default DeathBarChart;