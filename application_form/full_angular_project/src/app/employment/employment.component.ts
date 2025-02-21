
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-employment',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './employment.component.html',
  styleUrls: ['./employment.component.css']
})
export class EmploymentComponent implements OnInit {
  employmentForm: FormGroup;

  constructor(private fb: FormBuilder) {
    // Initialize the form with FormBuilder
    this.employmentForm = this.fb.group({
      companyName: ['', Validators.required],
      jobTitle: ['', Validators.required],
      startDate: ['', Validators.required],
      endDate: ['', Validators.required],
      responsibilities: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    // Any initialization logic can go here
  }

  onSubmit(): void {
    if (this.employmentForm.valid) {
      console.log('Employment Details:', this.employmentForm.value);
      // Here you can handle the form submission, e.g., sending data to a server
    } else {
      console.log('Form is invalid');
    }
  }
}
