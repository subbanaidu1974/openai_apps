
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';

@Component({
  selector: 'app-spousecoapplicant',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './spousecoapplicant.component.html',
  styleUrls: ['./spousecoapplicant.component.css']
})
export class SpouseCoApplicantComponent implements OnInit {
  spouseCoApplicantForm: FormGroup;

  constructor(private formBuilder: FormBuilder) {
    // Initialize the form group
    
    this.spouseCoApplicantForm = this.formBuilder.group({
      firstName: ['', [Validators.required, Validators.maxLength(50)]],
      lastName: ['', [Validators.required, Validators.maxLength(50)]],
      dateOfBirth: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      phone: ['', [Validators.required, Validators.pattern(/^\d{10}$/)]],
      address: this.formBuilder.group({
        street: ['', Validators.required],
        city: ['', Validators.required],
        state: ['', Validators.required],
        zip: ['', [Validators.required, Validators.pattern(/^\d{5}$/)]]
      })
    });
  }

  ngOnInit(): void {
    // Any additional initialization logic can go here
  }

  // Method to handle form submission
  onSubmit(): void {
    if (this.spouseCoApplicantForm.valid) {
      console.log('Form Submitted!', this.spouseCoApplicantForm.value);
      // Handle the form submission logic here (e.g., send data to the server)
    } else {
      console.log('Form is invalid');
    }
  }

  // Getter for easy access to form controls
  get formControls() {
    return this.spouseCoApplicantForm.controls;
  }
}

