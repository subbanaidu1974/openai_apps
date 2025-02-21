
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-applicant',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './applicant.component.html',
  styleUrls: ['./applicant.component.css']
})
export class ApplicantComponent implements OnInit {
  applicantForm: FormGroup;

  constructor(private fb: FormBuilder) {
    // Initialize the form with default values and validation
    this.applicantForm = this.fb.group({
      firstName: ['', [Validators.required, Validators.maxLength(50)]],
      lastName: ['', [Validators.required, Validators.maxLength(50)]],
      email: ['', [Validators.required, Validators.email]],
      phone: ['', [Validators.required, Validators.pattern(/^\d{10}$/)]],
      resume: [null, Validators.required]
    });
  }

  ngOnInit(): void {
    // Any initialization logic can go here
  }

  // Method to handle form submission
  onSubmit(): void {
    if (this.applicantForm.valid) {
      const applicantData = this.applicantForm.value;
      console.log('Applicant Data:', applicantData);
      // Here you can handle the form submission, e.g., send data to a service
    } else {
      console.log('Form is invalid');
    }
  }

  // Method to handle file input change
  onFileChange(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.applicantForm.patchValue({
        resume: file
      });
    }
  }
}
