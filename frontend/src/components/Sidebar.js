import React from 'react';
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
import InputLabel from '@material-ui/core/InputLabel';
import Select from '@material-ui/core/Select';

class Sidebar extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      scenario: null,
      selectedStartDate: null,
      selectedStartTime: null,
      selectedEndDate: null,
      selectedEndTime: null,
      gender: "All",
    };
  }

  sendData = (value) => {
    this.props.parentCallback(value);
  };

  handleStartDateChange = (date) => {
    this.setState({
      selectedStartDate: date,
    });
  };

   handleEndDateChange = (date) => {
    this.setState({
      selectedEndDate: date,
    });
  };

   handleStartTimeChange = (time) => {
    this.setState({
      selectedStartTime: time,
    });
  };

   handleEndTimeChange = (time) => {
    this.setState({
      selectedEndTime: time,
    });
  };

   handleGenderChange = (event) => {
    this.setState({
      gender: event.target.value,
    });
  };

  handleScenarioChange = (event) => {
    this.setState({
      scenario: event.target.value,
    });
    this.sendData(event.target.value)
  };

  // const handleChange = (event) => {

  // }

   clearFilters = ()=> {
     this.setState({
      selectedStartDate: null,
      selectedStartTime: null,
      selectedEndDate: null,
      selectedEndTime: null,
      gender: null
     })
  }

  render() {
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

      <Grid>
        {/* scenario selection */}
        <FormControl component="fieldset">
          <FormLabel component="legend">Scenario</FormLabel>
          <RadioGroup aria-label="scenario" name="scenario" value={this.state.scenario} onChange={this.handleScenarioChange}>
            <FormControlLabel value="Victoria Covid" control={<Radio />} label="Victoria Covid" />
            <FormControlLabel value="Tweet Heatmap" control={<Radio />} label="Tweet Heatmap" />
          </RadioGroup>
        </FormControl>
      </Grid>

      <Grid container justify="space-around">
      <KeyboardDatePicker
          disableToolbar
          variant="inline"
          format="MM/dd/yyyy"
          margin="normal"
          id="date-picker-inline"
          label="Start date"
          value={this.state.selectedStartDate}
          onChange={this.handleStartDateChange}
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
          value={this.state.selectedEndDate}
          onChange={this.handleEndDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change date',
          }}
        />
        <KeyboardTimePicker
          margin="normal"
          id="time-picker"
          label="Start time"
          value={this.state.selectedStartTime}
          onChange={this.handleStartTimeChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        />
        <KeyboardTimePicker
          margin="normal"
          id="time-picker"
          label="End time"
          value={this.state.selectedEndTime}
          onChange={this.handleEndTimeChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        />

    {/* gender selection */}
      <FormControl >
        <InputLabel htmlFor="gender-native-simple">Gender</InputLabel>
        <Select
          native
          value={this.state.gender}
          onChange={this.handleGenderChange}
          inputProps={{
            name: 'gender',
            id: 'gender-native-simple',
          }}
        >
          <option aria-label="None" value="" />
          <option value={"All"}>All</option>
          <option value={"Male"}>Male</option>
          <option value={"Female"}>Female</option>
        </Select>
      </FormControl>
      </Grid>

  <Grid>
    <Typography id="range-slider" gutterBottom>
      Age range
    </Typography>
    <Slider
      defaultValue={[10, 40]}
      onChange={this.handleChange}
      valueLabelDisplay="on"
      aria-labelledby="range-slider"
      min={0}
      max={100}
      getAriaValueText={this.valuetext}
      marks
    />
</Grid>

<Grid>
<Button variant="outlined" color="primary">
  Apply
</Button>
<Button variant="outlined" color="primary"
 onClick={this.clearFilters}>
  Clear
</Button>
</Grid>
</MuiPickersUtilsProvider>
    </Menu>
  );
};
}

export default Sidebar;