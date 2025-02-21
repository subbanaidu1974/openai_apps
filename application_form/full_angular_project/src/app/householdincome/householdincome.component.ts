
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-household-income',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './householdincome.component.html',
  styleUrls: ['./householdincome.component.css']
})
export class HouseholdIncomeComponent implements OnInit {
  householdIncomeForm: FormGroup;

  constructor(private fb: FormBuilder) {
    // Initialize the form
    this.householdIncomeForm = this.fb.group({
      incomeSources: this.fb.array([]),
    });
  }

  ngOnInit(): void {
    // Optionally, you can initialize the form with default values
    this.addIncomeSource(); // Add an initial income source
  }

  get incomeSources() {
    return this.householdIncomeForm.get('incomeSources');
  }

  addIncomeSource(): void {
    const incomeSourceGroup = this.fb.group({
      source: ['', Validators.required],
      amount: [0, [Validators.required, Validators.min(0)]],
    });
    // this.incomeSources.push(incomeSourceGroup);
  }

  removeIncomeSource(index: number): void {
    // this.incomeSources.removeAt(index);
  }

  onSubmit(): void {
    if (this.householdIncomeForm.valid) {
      console.log('Form Submitted!', this.householdIncomeForm.value);
      // Handle form submission, e.g., send data to a server
    } else {
      console.log('Form is invalid');
    }
  }
}

