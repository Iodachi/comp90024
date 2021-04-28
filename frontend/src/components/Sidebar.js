import React, { Component } from 'react';
import { bubble as Menu } from 'react-burger-menu';
import './Sidebar.css'

export class Sidebar extends Component {
  render(){
  return (
    <Menu>
      <a className="menu-item" href="/">
        Home
      </a>
    </Menu>
  );}
};

export default Sidebar;