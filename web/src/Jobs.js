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
        <td><a href={`/job/${j.jid}`}>{j.job_title}</a></td>
        <td><a href={`/company/${j.cid}`}>{j.company_name}</a></td>
        <td>{j.job_avg_salary > 0 ? j.job_avg_salary : '-'}</td>
        <td>{j.job_avg_rating ? j.job_avg_rating : '-'}</td>
      </tr>
    ));
  }

  sortRows(type) {
    let rows = this.state.jobs.slice(0);
    const ascending = this.state.sortAscending;
    switch(type) {
      case "title":
        if (!ascending) {
          rows.sort((a,b) => (a.job_title.toLowerCase() > b.job_title.toLowerCase()) ? 1 : ((b.job_title.toLowerCase() > a.job_title.toLowerCase()) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.job_title.toLowerCase() > b.job_title.toLowerCase()) ? -1 : ((b.job_title.toLowerCase() > a.job_title.toLowerCase()) ? 1 : 0));
        }
        break;
      case "company":
        if (!ascending) {
          rows.sort((a,b) => (a.company_name.toLowerCase() > b.company_name.toLowerCase()) ? 1 : ((b.company_name.toLowerCase() > a.company_name.toLowerCase()) ? -1 : 0));
        } else {
          rows.sort((a,b) => (a.company_name.toLowerCase() > b.company_name.toLowerCase()) ? -1 : ((b.company_name.toLowerCase() > a.company_name.toLowerCase()) ? 1 : 0));
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
              <th class="job-title" onClick={() => this.sortRows("title")}>Title</th>
              <th class="company-name" onClick={() => this.sortRows("company")}>Company</th>
              <th class="salary" onClick={() => this.sortRows("salary")}>Avg. Salary</th>
              <th class="rating" onClick={() => this.sortRows("rating")}>Avg. Rating</th>
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
