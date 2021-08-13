import React from "react";
import Chart from "react-google-charts";
import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';

export default class Company extends React.Component {
  state = {
    avg_rating: null,
    avg_salary: null,
    max_salary: null,
    min_salary: null,
    mmr: null,
    mmr_rank: null,
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
          mmr_rank: result.company_mmr_rank,
          name: result.company_name,
          jobs: result.jobs,
          hires_by_term: result.hires_by_term,
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
        this.setState({ hires_by_term: hires });
      })
      .catch((e) => {
        console.log(e);
      });
  }

  tableRows() {
    return this.state.jobs.map((j) => (
      <tr key={`job-${j.jid}`}>
        <td>
          <a href={`/job/${j.jid}`}>{j.job_title}</a>
        </td>
        <td>{j.job_avg_salary > 0 ? "$" + j.job_avg_salary : "N/A"}</td>
        <td>{j.job_avg_rating ? j.job_avg_rating : "N/A"}</td>
      </tr>
    ));
  }

  render() {
    return (
      <>
        <div class="company-header">
            <span class="company-name">{this.state.name}</span>
            <span class="badge">{`# ${this.state.mmr_rank} Rank`}</span>
        </div>
        <CardGroup>
          <Card className="text-card">
            <Card.Body>
              <Card.Title>MMR</Card.Title>
              <Card.Text>
                {this.state.mmr ? <h3>{this.state.mmr}</h3> : 'N/A'}
              </Card.Text>
            </Card.Body>
          </Card>
          <Card className="text-card">
            <Card.Body>
              <Card.Title>Average Rating</Card.Title>
              <Card.Text>
                {this.state.avg_rating ? <h3>{this.state.avg_rating}</h3> : 'N/A'}
              </Card.Text>
            </Card.Body>
          </Card>
          <Card className="text-card">
            <Card.Body>
              <Card.Title>Average Salary</Card.Title>
              <Card.Text>
                {this.state.avg_salary ? <><span class="company-info-salary">${this.state.avg_salary}</span>/hr</> : 'N/A'}
                <br></br>
                ({`$${this.state.min_salary ? this.state.min_salary: '_'}`}
                -
                {`$${this.state.max_salary ? this.state.max_salary : '_'}`})
              </Card.Text>
            </Card.Body>
          </Card>
        </CardGroup>
        <Card>
          <Card.Body>
          <Card.Title>Hires By Work Term</Card.Title>
          <div className="piechart-card">
          <Chart
                id="chart_div"
                width={'400px'}
                height={'400px'}
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
                  chartArea: {
                    height: '100%',
                    width: '100%',
                    top: 10,
                    left: 10,
                    right: 10,
                    bottom: 10,
                  },
                  height: '100%',
                  width: '100%'
                }}
                rootProps={{ 'data-testid': '1' }}
              />
          </div>
          </Card.Body>
        </Card>
        <h4 class="sub-header">Past Jobs</h4>
        <table class="table">
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Salary (CAD/hr)</th>
              <th>Rating(/5)</th>
            </tr>
          </thead>
          <tbody>{this.tableRows()}</tbody>
        </table>
      </>
    );
  }
}
