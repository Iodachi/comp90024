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

import { Button, ButtonGroup, Box, Switch, FormControl, FormLabel, FormControlLabel, Radio, RadioGroup} from '@material-ui/core'
import 'date-fns';
import Popup from 'reactjs-popup';

import history from '../history'
import TopWordBarChart from './TopWordBarChart';
import { withStyles } from '@material-ui/core/styles';

const AntSwitch = withStyles((theme) => ({
  root: {
    width: 28,
    height: 16,
    padding: 0,
    display: 'flex',
  },
  switchBase: {
    padding: 2,
    color: theme.palette.grey[500],
    '&$checked': {
      transform: 'translateX(12px)',
      color: theme.palette.common.white,
      '& + $track': {
        opacity: 1,
        backgroundColor: theme.palette.primary.main,
        borderColor: theme.palette.primary.main,
      },
    },
  },
  thumb: {
    width: 12,
    height: 12,
    boxShadow: 'none',
  },
  track: {
    border: `1px solid ${theme.palette.grey[500]}`,
    borderRadius: 16 / 2,
    opacity: 1,
    backgroundColor: theme.palette.common.white,
  },
  checked: {},
}))(Switch);

class Sidebar extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      scenario: null,
      selectedStartDate: new Date('2020-10-01T00:00:00'),
      selectedEndDate: new Date('2021-05-01T00:00:00'),
      gender: "All",
      isWordOrTag: false,
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

  handleSwitchChange = (event) => {
    this.setState({
      isWordOrTag: event.target.checked
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
            <FormControlLabel value="Tweet Top words" control={<Radio />} label="Tweet Top Words/Tags" />
          </RadioGroup>
        </FormControl>
      </Grid>

  <Box visibility={this.state.scenario === "Tweet Top words" ? "visible": "hidden"}>

  <Grid component="label" container alignItems="center" spacing={2}>
          <Grid item >word</Grid>
          <Grid item>
            <AntSwitch checked={this.state.isWordOrTag} onChange={this.handleSwitchChange} name="isWordOrTag" />
          </Grid>
          <Grid item>tag</Grid>
        </Grid>

      <Grid container justify="space-around" >
      <KeyboardDatePicker
          disableToolbar
          variant="inline"
          format="MM/dd/yyyy"
          margin="normal"
          id="start-date-picker-inline"
          label="Start date"
          maxDate={this.state.selectedEndDate}
          value={this.state.selectedStartDate}
          onChange={this.handleStartDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change date',
          }}
        />
        <KeyboardTimePicker
          margin="normal"
          id="start-time-picker"
          label="Start time"
          value={this.state.selectedStartDate}
          onChange={this.handleStartDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        />
        <KeyboardDatePicker
          disableToolbar
          variant="inline"
          format="MM/dd/yyyy"
          margin="normal"
          id="end-date-picker-inline"
          label="End date"
          minDate={this.state.selectedStartDate}
          value={this.state.selectedEndDate}
          onChange={this.handleEndDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change date',
          }}
        />
        <KeyboardTimePicker
          margin="normal"
          id="end-time-picker"
          label="End time"
          value={this.state.selectedEndDate}
          onChange={this.handleEndDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        />
        </Grid>

    {/* gender selection
    <Grid>
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
</Grid> */}
    <Grid>
      <Popup trigger={<Button variant="outlined" color="primary">
        Apply
      </Button>} modal>
      <TopWordBarChart 
        startDate={this.state.selectedStartDate} 
        endDate={this.state.selectedEndDate}
        isWordOrTag={this.state.isWordOrTag}/>
      </Popup>
    </Grid>

    </Box>
    </MuiPickersUtilsProvider>
    </Menu>

  );
};
}

export default Sidebar;