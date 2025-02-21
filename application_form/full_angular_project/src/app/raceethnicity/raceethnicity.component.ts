
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-race-ethnicity',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './raceethnicity.component.html',
  styleUrls: ['./raceethnicity.component.css']
})
export class RaceEthnicityComponent implements OnInit {
  raceEthnicityForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.raceEthnicityForm = this.fb.group({
      race: ['', Validators.required],
      ethnicity: ['', Validators.required],
      other: ['']
    });
  }

  ngOnInit(): void {
    // Initialization logic can go here if needed
  }

  onSubmit(): void {
    if (this.raceEthnicityForm.valid) {
      console.log('Form Submitted!', this.raceEthnicityForm.value);
      // Handle form submission, e.g., send data to a service
    } else {
      console.log('Form is invalid');
    }
  }
}
