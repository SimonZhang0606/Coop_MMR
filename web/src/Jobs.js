import React from 'react';

export default class Jobs extends React.Component {
  state = {
    jobs: [],
    sortAscending: true
  };

  // Fetch jobs
  constructor() {
    super();
    fetch("http://localhost:5000/jobs")
      .then((response) => response.json())
      .then((result) => {
        this.setState({ jobs: result.jobs });
      })
      .catch((e) => {
        console.log(e);
      });
  }

  tableRows() {
    return this.state.jobs.map((j) => (
      <tr key={`job-${j.jid}`}>
        <td>{j.job_title}</td>
        <td><a href={`/company/${j.cid}`}>{j.company_name}</a></td>
        <td>{j.job_avg_salary > 0 ? j.job_avg_salary : null}</td>
        <td>{j.job_avg_rating}</td>
      </tr>
    ));
  }

  sortRows(type) {
    let rows = this.state.jobs.slice(0);
    const ascending = this.state.sortAscending;
    switch(type) {
      case "title":
        if (!ascending) {
          rows.sort((a,b) => (a.job_title > b.job_title) ? 1 : ((b.job_title > a.job_title) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.job_title > b.job_title) ? -1 : ((b.job_title > a.job_title) ? 1 : 0));
        }
        break;
      case "company":
        if (!ascending) {
          rows.sort((a,b) => (a.company_name > b.company_name) ? 1 : ((b.company_name > a.company_name) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.company_name > b.company_name) ? -1 : ((b.company_name > a.company_name) ? 1 : 0));
        }
        break;
      case "salary":
        if (!ascending) {
          rows.sort((a,b) => (a.job_avg_salary > b.job_avg_salary) ? 1 : ((b.job_avg_salary > a.job_avg_salary) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.job_avg_salary > b.job_avg_salary) ? -1 : ((b.job_avg_salary > a.job_avg_salary) ? 1 : 0));
        }
        break;
      case "rating":
        if (!ascending) {
          rows.sort((a,b) => (a.job_avg_rating > b.job_avg_rating) ? 1 : ((b.job_avg_rating > a.job_avg_rating ) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.job_avg_rating > b.job_avg_rating ) ? -1 : ((b.job_avg_rating > a.job_avg_rating) ? 1 : 0));
        }
        break;
    }
    this.setState({
      jobs: rows,
      sortAscending: !ascending
    });
  }

  render() {
    return (
      <>
        <table>
          <thead>
            <tr>
              <th onClick={() => this.sortRows("title")}>Title</th>
              <th onClick={() => this.sortRows("company")}>Company</th>
              <th onClick={() => this.sortRows("salary")}>Avg. Salary</th>
              <th onClick={() => this.sortRows("rating")}>Avg. Rating</th>
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
