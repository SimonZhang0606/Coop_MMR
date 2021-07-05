import React from 'react';
import { Link } from "react-router-dom";

export default class Companies extends React.Component {
  state = {
    companies: [],
    sortAscending: false
  };

  constructor() {
    super();
    fetch("http://localhost:5000/companies")
      .then((response) => response.json())
      .then((result) => {
        this.setState({ companies: result.companies });
      })
      .catch((e) => {
        console.log(e);
      });
  }

  tableRows() {
    return this.state.companies.map((c) => (
      <tr key={`company-${c.cid}`}>
        <td><a href={`/company/${c.cid}`}>{c.company_name}</a></td>
        <td>{c.company_avg_salary > 0 ? c.company_avg_salary : null}</td>
        <td>{c.company_avg_rating}</td>
        <td>{c.company_mmr}</td>
      </tr>
    ));
  }

  sortRows(type) {
    let rows = this.state.companies.slice(0);
    const ascending = this.state.sortAscending;
    switch(type) {
      case "company":
        if (!ascending) {
          rows.sort((a,b) => (a.company_name > b.company_name) ? 1 : ((b.company_name > a.company_name) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.company_name > b.company_name) ? -1 : ((b.company_name > a.company_name) ? 1 : 0));
        }
        break;
      case "salary":
        if (!ascending) {
          rows.sort((a,b) => (a.company_avg_salary > b.company_avg_salary) ? 1 : ((b.company_avg_salary > a.company_avg_salary) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.company_avg_salary > b.company_avg_salary) ? -1 : ((b.company_avg_salary > a.company_avg_salary) ? 1 : 0));
        }
        break;
      case "rating":
        if (!ascending) {
          rows.sort((a,b) => (a.company_avg_rating > b.company_avg_rating) ? 1 : ((b.company_avg_rating > a.company_avg_rating ) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.company_avg_rating > b.company_avg_rating ) ? -1 : ((b.company_avg_rating > a.company_avg_rating) ? 1 : 0));
        }
        break;
      case "mmr":
        if (!ascending) {
          rows.sort((a,b) => (a.company_mmr > b.company_mmr) ? 1 : ((b.company_mmr > a.company_mmr) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.company_mmr > b.company_mmr) ? -1 : ((b.company_mmr > a.company_mmr) ? 1 : 0));
        }
        break;
    }
    this.setState({
      companies: rows,
      sortAscending: !ascending
    });
  }

  render() {
    return (
      <>
        <table>
          <thead>
            <tr>
              <th onClick={() => this.sortRows("company")}>Company</th>
              <th onClick={() => this.sortRows("salary")}>Avg. Salary</th>
              <th onClick={() => this.sortRows("rating")}>Avg. Rating</th>
              <th onClick={() => this.sortRows("mmr")}>MMR</th>
            </tr>
          </thead>
          <tbody>
            {this.tableRows()}
            <tr></tr>
          </tbody>
        </table>
      </>
    );
  }
}
