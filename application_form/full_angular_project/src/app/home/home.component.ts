
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  homeForm: FormGroup;

  constructor(private fb: FormBuilder) {
    // Initialize the form group
    this.homeForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      message: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    // Any additional initialization logic can go here
  }

  onSubmit(): void {
    if (this.homeForm.valid) {
      console.log('Form Submitted!', this.homeForm.value);
      // Handle form submission logic here
    } else {
      console.log('Form is invalid');
    }
  }
}
