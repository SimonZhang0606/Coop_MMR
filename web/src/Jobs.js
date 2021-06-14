import React from 'react';

export default class Jobs extends React.Component {
  jobs = []

  // Fetch jobs
  componentDidMount() {
    fetch("http://localhost:5000/jobs")
      .then(response => response.json())
      .then(result => {
        this.jobs = result
      })
      .catch(e => {
        console.log(e);
      });
  }

  tableRows() {
    return this.jobs.map(j => (
      <tr>
        <td>{j.job_title}</td>
        <td>{j.company_name}</td>
        <td>{j.avg_salary}</td>
        <td>{j.avg_rating}</td>
      </tr>
    ))
  }

  render() {
    return (
      <>
      <h1>Jobs</h1>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Company</th>
            <th>Avg. Salary</th>
            <th>Avg. Rating</th>
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