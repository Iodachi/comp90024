import React from 'react'
import DeathBarChart from '../components/DeathBarChart'
import EmploymentBarChart from '../components/EmploymentBarChart'
 
function Analysis() {
 
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