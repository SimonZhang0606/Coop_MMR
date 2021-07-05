import React from "react";
import Chart from "react-google-charts";

export default class Company extends React.Component {
  state = {
    avg_rating: null,
    avg_salary: null,
    max_salary: null,
    min_salary: null,
    mmr: null,
    name: null, 
    jobs: [],
    hires_by_term: {},
  };

  constructor(props) {
    super();
    let cid = props.match.params.cid;
    fetch(`http://localhost:5000/companies/${cid}`)
      .then((response) => response.json())
      .then((result) => {
        this.setState({ 
          avg_rating: result.company_avg_rating,
          avg_salary: result.company_avg_salary,
          max_salary: result.company_max_salary,
          min_salary: result.company_min_salary,
          mmr: result.company_mmr,
          name: result.company_name,
          jobs: result.jobs,
          hires_by_term: result.hires_by_term
        });
        let hires = {};
        for (const obj of result.hires_by_term) {
          hires[obj.term_num] = obj.hires;
        }
        for (let i = 1; i < 7; i++) {
          if (!(i in hires)) {
            hires[i] = 0;
          }
        }
        this.setState({hires_by_term: hires});
      })
      .catch((e) => {
        console.log(e);
      });
  }

  tableRows() {
    return this.state.jobs.map((j) => (
      <tr key={`job-${j.jid}`}>
        <td>{j.job_title}</td>
        <td>{j.job_avg_salary > 0 ? j.job_avg_salary : null}</td>
        <td>{j.job_avg_rating}</td>
      </tr>
    ));
  }

  render() {
    return (
      <>
        <h2>{this.state.name}</h2>
        <p>{`Rating: ${this.state.avg_rating}`}</p>
        <p>{`Salary: ${this.state.avg_salary}`}</p>
        <p>{`Max salary: ${this.state.max_salary}`}</p>
        <p>{`Min salary: ${this.state.min_salary}`}</p>
        <p>{`MMR: ${this.state.mmr}`}</p>
        <h3>Past Jobs</h3>
        <table>
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Avg. Salary</th>
              <th>Avg. Rating</th>
            </tr>
          </thead>
          <tbody>
            {this.tableRows()}
          </tbody>
        </table>
        <h3>Co-ops Breakdown By Work Term</h3>
        <Chart
          width={'500px'}
          height={'500px'}
          chartType="PieChart"
          loader={<div>Loading Chart</div>}
          data={[
            ['Term', 'Number'],
            ['1', this.state.hires_by_term[1]],
            ['2', this.state.hires_by_term[2]],
            ['3', this.state.hires_by_term[3]],
            ['4', this.state.hires_by_term[4]],
            ['5', this.state.hires_by_term[5]],
            ['6', this.state.hires_by_term[6]],
          ]}
          options={{
            title: '',
          }}
          rootProps={{ 'data-testid': '1' }}
        />
      </>
    );
  }
}
