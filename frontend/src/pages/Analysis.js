import React from 'react'
import { Chart } from 'react-charts'
import DeathBarChart from '../components/DeathBarChart'
import EmploymentBarChart from '../components/EmploymentBarChart'
 
function Analysis() {
  const data = React.useMemo(
    () => [
      {
        label: 'Covid 19',
        data: [[1, 2], [2, 4], [3, 2], [4, 7]]
      },
    ],
    []
  )
 
  const series = React.useMemo(
    () => ({
      type: 'bar'
    }),
    []
  )

  const axes = React.useMemo(
    () => [
      { primary: true, type: 'linear', position: 'bottom' },
      { type: 'linear', position: 'left' }
    ],
    []
  )
 
  return (
    <div>
      <div>
        <DeathBarChart/>
    </div>
    <div>
      <EmploymentBarChart/>
    </div>
</div>
  )
}

export default Analysis;