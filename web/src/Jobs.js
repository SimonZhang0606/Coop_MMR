import React from 'react';

export default class Jobs extends React.Component {
  jobs = [{job_title: 'Full-Stack Software Developer', company_name: 'SAP', avg_salary: '55.5', avg_rating: '3'}]

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