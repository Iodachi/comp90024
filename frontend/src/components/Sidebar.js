import React, { useState } from 'react';
import { bubble as Menu } from 'react-burger-menu';
import './Sidebar.css'
import 'react-calendar/dist/Calendar.css';
import Grid from '@material-ui/core/Grid';
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker,
  KeyboardTimePicker,
} from '@material-ui/pickers';

import { Button, ButtonGroup } from '@material-ui/core'
import 'date-fns';

import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';

import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';

import history from '../history'

export default function Sidebar() {
  const [selectedStartDate, setStartDate] = useState(null);
  const [selectedEndDate, setEndDate] = useState(null);
  const [selectedStartTime, setStartTime] = useState(null);
  const [selectedEndTime, setEndTime] = useState(null);
  const [selectedValue, setSelectedGender] = React.useState('a');

  const handleStartDateChange = (date) => {
    setStartDate(date);
  };

  const handleEndDateChange = (date) => {
    setEndDate(date);
  };

  const handleStartTimeChange = (time) => {
    setStartTime(time);
  };

  const handleEndTimeChange = (time) => {
    setEndTime(time);
  };

  const handleChange = (event) => {
    setSelectedGender(event.target.value);
  };

  const clearFilters = ( )=> {
    setStartDate(null)
    setEndDate(null);
    setStartTime(null);
    setEndTime(null);
    setSelectedGender(null);
  }
  function valuetext(value) {
    return `${value}`;
  }

  return (
    <Menu>
      <ButtonGroup fullWidth variant="text" color="primary" aria-label="text primary button group">
      <Button variant="outlined" color="primary"
        onClick={() => history.push('/')}>
        Map
      </Button>
      <Button variant="outlined" color="primary"
        onClick={() => history.push('/Analysis')}>
        Analysis
      </Button>
      </ButtonGroup>

      <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <Grid container justify="space-around">
      <KeyboardDatePicker
          disableToolbar
          variant="inline"
          format="MM/dd/yyyy"
          margin="normal"
          id="date-picker-inline"
          label="Start date"
          value={selectedStartDate}
          onChange={handleStartDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change date',
          }}
        />
        <KeyboardDatePicker
          disableToolbar
          variant="inline"
          format="MM/dd/yyyy"
          margin="normal"
          id="date-picker-inline"
          label="End date"
          value={selectedEndDate}
          onChange={handleEndDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change date',
          }}
        />
        <KeyboardTimePicker
          margin="normal"
          id="time-picker"
          label="Start time"
          value={selectedStartTime}
          onChange={handleStartTimeChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        />
        <KeyboardTimePicker
          margin="normal"
          id="time-picker"
          label="End time"
          value={selectedEndTime}
          onChange={handleEndTimeChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        />
         </Grid>


  <Grid>
    {/* gender selection */}
    <FormControl component="fieldset">
      <FormLabel component="legend">Gender</FormLabel>
        <RadioGroup aria-label="gender" name="gender1" value={selectedValue} onChange={handleChange}>
          <FormControlLabel value="all" control={<Radio />} label="All" />
          <FormControlLabel value="female" control={<Radio />} label="Female" />
          <FormControlLabel value="male" control={<Radio />} label="Male" />
      </RadioGroup>
    </FormControl>
  </Grid>

  <Grid>
    <Typography id="range-slider" gutterBottom>
      Age range
    </Typography>
    <Slider
      defaultValue={[10, 40]}
      onChange={handleChange}
      valueLabelDisplay="on"
      aria-labelledby="range-slider"
      min={0}
      max={100}
      getAriaValueText={valuetext}
      marks
    />
</Grid>

<Grid>
<Button variant="outlined" color="primary">
  Apply
</Button>
<Button variant="outlined" color="primary"
 onClick={clearFilters}>
  Clear
</Button>
</Grid>
</MuiPickersUtilsProvider>
    </Menu>
  );
};