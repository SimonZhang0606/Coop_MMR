import React from "react";

export default class Companies extends React.Component {
  state = {
    companies: [],
    sortAscending: false,
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
        <td>
          <a href={`/company/${c.cid}`}>{c.company_name}</a>
        </td>
        <td>{c.company_avg_salary > 0 ? "$" + c.company_avg_salary : "-"}</td>
        <td>{c.company_avg_rating ? c.company_avg_rating : "-"}</td>
        <td>{c.company_mmr}</td>
      </tr>
    ));
  }

  sortRows(type) {
    let rows = this.state.companies.slice(0);
    const ascending = this.state.sortAscending;
    switch (type) {
      case "company":
        if (!ascending) {
          rows.sort((a, b) =>
            a.company_name.toLowerCase() > b.company_name.toLowerCase()
              ? 1
              : b.company_name.toLowerCase() > a.company_name.toLowerCase()
              ? -1
              : 0
          );
        } else {
          rows.sort((a, b) =>
            a.company_name.toLowerCase() > b.company_name.toLowerCase()
              ? -1
              : b.company_name.toLowerCase() > a.company_name.toLowerCase()
              ? 1
              : 0
          );
        }
        break;
      case "salary":
        if (!ascending) {
          rows.sort((a, b) =>
            a.company_avg_salary > b.company_avg_salary
              ? 1
              : b.company_avg_salary > a.company_avg_salary
              ? -1
              : 0
          );
        } else {
          rows.sort((a, b) =>
            a.company_avg_salary > b.company_avg_salary
              ? -1
              : b.company_avg_salary > a.company_avg_salary
              ? 1
              : 0
          );
        }
        break;
      case "rating":
        if (!ascending) {
          rows.sort((a, b) =>
            a.company_avg_rating > b.company_avg_rating
              ? 1
              : b.company_avg_rating > a.company_avg_rating
              ? -1
              : 0
          );
        } else {
          rows.sort((a, b) =>
            a.company_avg_rating > b.company_avg_rating
              ? -1
              : b.company_avg_rating > a.company_avg_rating
              ? 1
              : 0
          );
        }
        break;
      case "mmr":
        if (!ascending) {
          rows.sort((a, b) =>
            a.company_mmr > b.company_mmr
              ? 1
              : b.company_mmr > a.company_mmr
              ? -1
              : 0
          );
        } else {
          rows.sort((a, b) =>
            a.company_mmr > b.company_mmr
              ? -1
              : b.company_mmr > a.company_mmr
              ? 1
              : 0
          );
        }
        break;
      default:
        break;
    }
    this.setState({
      companies: rows,
      sortAscending: !ascending,
    });
  }

  render() {
    return (
      <>
        <table class="table">
          <thead class="thead-dark">
            <tr>
              <th
                scope="col"
                class="company"
                onClick={() => this.sortRows("company")}
              >
                Company
              </th>
              <th
                scope="col"
                class="salary"
                onClick={() => this.sortRows("salary")}
              >
                Salary (CAD/hr)
              </th>
              <th
                scope="col"
                class="rating"
                onClick={() => this.sortRows("rating")}
              >
                Rating (/5)
              </th>
              <th scope="col" class="mmr" onClick={() => this.sortRows("mmr")}>
                MMR
              </th>
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
