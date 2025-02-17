import React, { useState } from "react";
import "./LeadForm.css";
import axios from 'axios';

const LeadForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "", 
    loanAmount: "",
    loanTerm: "",
    interestRate: "5.99",
    monthlyIncome: "",
  });

  const [result, setResult] = useState(null);
  const [step, setStep] = useState(1);
  const [showSuccess, setShowSuccess] = useState(false);

  const calculateLoan = () => {
    const principal = parseFloat(formData.loanAmount);
    const years = parseFloat(formData.loanTerm);
    const rate = parseFloat(formData.interestRate) / 100 / 12;
    const numberOfPayments = years * 12;

    const monthlyPayment = (
      (principal * rate * Math.pow(1 + rate, numberOfPayments)) /
      (Math.pow(1 + rate, numberOfPayments) - 1)
    ).toFixed(2);

    const totalPayment = (monthlyPayment * numberOfPayments).toFixed(2);
    const totalInterest = (totalPayment - principal).toFixed(2);

    return { monthlyPayment, totalPayment, totalInterest };
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    console.log(`Input changed: ${name} = ${value}`);
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const resetForm = () => {
    setFormData({
      name: "",
      email: "",
      phone: "",
      loanAmount: "",
      loanTerm: "",
      interestRate: "5.99",
      monthlyIncome: "",
    });
    setResult(null);
    setStep(1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate loan calculation fields first
    if (!formData.loanAmount || !formData.loanTerm || !formData.interestRate) {
      console.error("Please fill in all loan calculation fields");
      return;
    }

    const calculations = calculateLoan();
    setResult(calculations);
    
    if (step === 1) {
      setStep(2);
      return;
    }

    // Only attempt to submit lead data if we're on step 2 and have contact info
    if (step === 2) {
      const leadData = {
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        loan_amount: parseFloat(formData.loanAmount),
        loan_term: parseInt(formData.loanTerm, 10),
        interest_rate: parseFloat(formData.interestRate),
        monthly_income: parseFloat(formData.monthlyIncome) || 0,
        message: "Lead from loan calculator",
      };

      console.log("Form Data:", leadData);

      // Check for required fields
      if (!leadData.name || !leadData.email || !leadData.phone || !leadData.loan_amount || !leadData.loan_term || !leadData.interest_rate) {
        console.error("Please fill in all required fields");
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:8000/api/leads/', leadData);
        console.log("Lead data submitted successfully:", response.data);
        setShowSuccess(true);
        resetForm();
        setTimeout(() => {
          setShowSuccess(false);
        }, 3000);
      } catch (error) {
        console.error("Error submitting lead data:", error.response ? error.response.data : error.message);
      }
    }
  };

  return (
    <div className="calculator-container">
      {showSuccess && (
        <div className={`success-popup ${!showSuccess ? 'hidden' : ''}`}>
          Your report request has been submitted successfully!
        </div>
      )}
      <div className="calculator-header">
        <h2>Loan Calculator</h2>
        <p className="subtitle">Get your personalized loan estimate today</p>
      </div>

      <div className="calculator-content">
        {step === 1 ? (
          <form onSubmit={handleSubmit} className="calculator-form">
            <div className="form-group">
              <label htmlFor="loanAmount">Loan Amount ($)</label>
              <input
                type="number"
                name="loanAmount"
                id="loanAmount"
                value={formData.loanAmount}
                onChange={handleInputChange}
                required
                placeholder="Enter loan amount"
                className="form-input"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="loanTerm">Loan Term (Years)</label>
                <input
                  type="number"
                  name="loanTerm"
                  id="loanTerm"
                  value={formData.loanTerm}
                  onChange={handleInputChange}
                  required
                  placeholder="Enter term"
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="interestRate">Interest Rate (%)</label>
                <input
                  type="number"
                  name="interestRate"
                  id="interestRate"
                  value={formData.interestRate}
                  onChange={handleInputChange}
                  step="0.01"
                  required
                  className="form-input"
                />
              </div>
            </div>

            <button type="submit" className="calculate-button">
              Calculate Payment
            </button>
          </form>
        ) : (
          <div className="results-container">
            <div className="result-summary">
              <div className="result-item">
                <h3>Monthly Payment</h3>
                <p className="amount">${result.monthlyPayment}</p>
              </div>
              <div className="result-item">
                <h3>Total Payment</h3>
                <p className="amount">${result.totalPayment}</p>
              </div>
              <div className="result-item">
                <h3>Total Interest</h3>
                <p className="amount">${result.totalInterest}</p>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="lead-capture-form">
              <h3>Get Your Detailed Report</h3>
              <div className="form-group">
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Full Name"
                  required
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="Email Address"
                  required
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  placeholder="Phone Number"
                  required
                  className="form-input"
                />
              </div>
              <button type="submit" className="submit-button">
                Get Free Report
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default LeadForm;
