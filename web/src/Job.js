import React from "react";
import Chart from "react-google-charts";

export default class Company extends React.Component {
  state = {
    jid: null, 
    cid: null,
    company_name: null,
    job_avg_rating: null, 
    job_avg_salary: null, 
    job_max_salary: null, 
    job_min_salary: null, 
    job_rating_rank: null, 
    job_salary_rank: null, 
    job_title: null,
    reviews: [], 
    tags: [],
    hires_by_term: {},
    review_headline: "",
    review_rating: 1,
    review_body: "",
  };

  constructor(props) {
    super();
    let jid = props.match.params.jid;
    fetch(`http://localhost:5000/jobs/${jid}`)
      .then((response) => response.json())
      .then((result) => {
        this.setState({ 
          jid: jid,
          cid: result.cid,
          company_name: result.company_name,
          job_avg_rating: result.job_avg_rating, 
          job_avg_salary: result.job_avg_salary, 
          job_max_salary: result.job_max_salary, 
          job_min_salary: result.job_min_salary, 
          job_rating_rank: result.job_rating_rank, 
          job_salary_rank: result.job_salary_rank, 
          job_title: result.job_title,
          reviews: result.reviews.slice(0), 
          tags: result.tags
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

  reviewRows() {
    return this.state.reviews.map((r) => (
      <div key={`key-${r.rid}`}>
        <h4>{`${r.rating} - ${r.headline}`}</h4>
        <p>{r.review_body}</p>
      </div>
    ));
  }

  handleSubmit(e) {
    e.preventDefault();
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        jid: this.state.jid,
        cid: this.state.cid,
        headline: this.state.review_headline,
        review_body: this.state.review_body,
        rating: this.state.review_rating
      })
    };
    fetch(`http://localhost:5000/jobs/${this.state.jid}/reviews`, requestOptions)
        .then(response => response.json());
  }

  handleChange(e, type) {
    switch(type) {
      case "review_headline":
        this.setState({
          review_headline: e.target.value
        })
        break;
      case "review_rating":
        this.setState({
          review_rating: e.target.value
        })
        break;
      case "review_body":
        this.setState({
          review_body: e.target.value
        })
        break;
    }
  }

  render() {
    return (
      <>
        <h1>{this.state.job_title}</h1>
        <h2>{this.state.company_name}</h2>
        <p>{`Rating: ${this.state.job_avg_rating ? this.state.job_avg_rating : 'N/A'}`}</p>
        <p>{`Salary: ${this.state.job_avg_salary ? this.state.job_avg_salary : 'N/A'}`}</p>
        <p>{`Max salary: ${this.state.job_max_salary ? this.state.job_max_salary : 'N/A'}`}</p>
        <p>{`Min salary: ${this.state.job_min_salary ? this.state.job_min_salary: 'N/A'}`}</p>
        <h3 class="sub-header">Breakdown of Hires By Work Term</h3>
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
        <h3 class="sub-header">Reviews</h3>
        <div>
        {this.reviewRows()}
        </div>
        <h3 class="sub-header">Leave a Review</h3>
        <form onSubmit={(e) => this.handleSubmit(e)}>
          <label>
            Summary<br></br>
            <input class="review-input" type="text" name="summary" onChange={(e) => this.handleChange(e, 'review_headline')}/><br></br>
          </label>
          <label>
            Rating (1-5)<br></br>
            <input class="review-input" type="number" name="rating" onChange={(e) => this.handleChange(e, 'review_rating')}/><br></br>
          </label>
          <label>
            Description <br></br>
            <textarea class="review-input" rows="10" name="description" onChange={(e) => this.handleChange(e, 'review_body')} /><br></br>
          </label>
          <input type="submit" value="Submit" />
        </form>
      </>
    );
  }
}
