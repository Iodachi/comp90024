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
import 'date-fns';

import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';

import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';

export default function Sidebar() {
  const [selectedDate, setSelectedDate] = useState(new Date('2021-01-01'));
  const [selectedValue, setSelectedValue] = React.useState('a');

  const handleDateChange = (date) => {
    setSelectedDate(date);
  };

  const handleChange = (event) => {
    setSelectedValue(event.target.value);
  };

  function valuetext(value) {
    return `${value}`;
  }

  return (
    <Menu>
      {/* <a className="menu-item" href="/">
        Home
      </a> */}
      {/* date and time picker */}
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <Grid container justify="space-around">
      <KeyboardDatePicker
          disableToolbar
          variant="inline"
          format="MM/dd/yyyy"
          margin="normal"
          id="date-picker-inline"
          label="Start date"
          value={selectedDate}
          onChange={handleDateChange}
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
          value={selectedDate}
          onChange={handleDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change date',
          }}
        />
        <KeyboardTimePicker
          margin="normal"
          id="time-picker"
          label="Start time"
          value={selectedDate}
          onChange={handleDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        />
        <KeyboardTimePicker
          margin="normal"
          id="time-picker"
          label="End time"
          value={selectedDate}
          onChange={handleDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        />
         </Grid>
    </MuiPickersUtilsProvider>


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
    </Menu>
  );
};