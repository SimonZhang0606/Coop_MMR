import React from "react";
import Chart from "react-google-charts";
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

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
    review_headline: null,
    review_rating: null,
    review_body: null,
    showing_review_modal: false,
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
      <Card key={`key-${r.rid}`} className="review-card">
        <Card.Header><b>{r.rating}</b> / 5</Card.Header>
        <Card.Body>
          <Card.Title>{r.headline}</Card.Title>
          <Card.Text>
            {r.review_body}
          </Card.Text>
        </Card.Body>
      </Card>
    ));
  }

  handleSubmit(e) {
    e.preventDefault();
    if (!(this.state.review_headline && this.state.review_body && this.state.review_rating)) return ;
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
        .then(response => response.json())
        .then(() => {
          fetch(`http://localhost:5000/jobs/${this.state.jid}`)
          .then((response) => response.json())
          .then((result) => {
            this.setState({
              job_avg_rating: result.job_avg_rating,
              job_rating_rank: result.job_rating_rank,
              job_salary_rank: result.job_salary_rank,
              reviews: result.reviews.slice(0), 
            });
          });
        });
      this.handleClose();
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

  showReviewModal (e) {
    console.log("showReviewModal");
    this.setState({
      showing_review_modal: true
    });
  }

  handleClose(e) {
    this.setState({
      showing_review_modal: false,
      review_headline: null,
      review_rating: null,
      review_body: null
    });
  }

  render() {
    return (
      <>
      <div>
        <span class="job-company-name">{this.state.company_name} - </span>
        <span class="job-title-name">{this.state.job_title}</span>
      </div>
        <CardGroup>
          <Card className="text-card">
            <Card.Body>
              <Card.Title>Average Rating</Card.Title>
              <Card.Text>
                {this.state.job_avg_rating ? <h3>{this.state.job_avg_rating}</h3> : 'N/A'}
              </Card.Text>
            </Card.Body>
          </Card>
          <Card className="text-card">
            <Card.Body>
              <Card.Title>Average Salary</Card.Title>
              <Card.Text>
                {this.state.job_avg_salary ? <><span class="company-info-salary">${this.state.job_avg_salary}</span>/hr</> : 'N/A'}
                <br></br>
                ({`$${this.state.job_min_salary ? this.state.job_min_salary: '_'}`}
                -
                {`$${this.state.job_max_salary ? this.state.job_max_salary : '_'}`})
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
        <div class="review-header">
          <span class="sub-header">Reviews</span>
          <Button
            variant="primary"
            onClick={this.showReviewModal.bind(this)}
          >
            Leave a Review
          </Button>
        </div>
        <div>
        {this.reviewRows()}
        </div>
        <Modal show={this.state.showing_review_modal} onHide={this.handleClose.bind(this)}>
        <Modal.Header closeButton>
          <Modal.Title>Review</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group >
            <Form.Label>Summary: </Form.Label>
            <Form.Control type="text" onChange={(e) => this.handleChange(e, 'review_headline')} value={this.state.review_headline}/>
          </Form.Group>
          <Form.Group >
            <Form.Label>Rating (1-5): </Form.Label>
            <Form.Control type="number" onChange={(e) => this.handleChange(e, 'review_rating')} value={this.state.review_rating}/>
          </Form.Group>
          <Form.Group >
            <Form.Label>Description </Form.Label>
            <Form.Control as="textarea" rows={10} onChange={(e) => this.handleChange(e, 'review_body')} value={this.state.review_body}/>
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={this.handleClose.bind(this)}>
            Close
          </Button>
          <Button variant="primary" onClick={(e) => this.handleSubmit(e)}>
            Submit
          </Button>
        </Modal.Footer>
      </Modal>

      </>
    );
  }
}
