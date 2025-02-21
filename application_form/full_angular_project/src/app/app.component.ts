import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'My Angular App';
  myForm: FormGroup;
  submitted: Boolean = false;

  constructor(private fb: FormBuilder,private router: Router) {
    this.title = 'DPA Application';
    // Initialize the form using FormBuilder
    // this.myForm = this.fb.group({
    //   firstName: ['', Validators.required],
    //   lastName: ['', Validators.required],
    //   email: ['', [Validators.required, Validators.email]]      
    // });
  }


  ngOnInit(): void {
    // Any initialization logic can go here
  }

  // onSubmit(): void {
  //   console.log(this.myForm.valid);
  //   this.router.navigate(['/home'])
    
    // if (this.myForm.valid) {
    //   console.log('Form Submitted!', this.myForm.value);
    //   this.router.navigateByUrl('/applicant');
        
    //   // Handle form submission logic here
    // } else {
    //   console.log('Form is invalid');
    // }
  // }
}
