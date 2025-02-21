
// src/app/otherhouseholdmembers/otherhouseholdmembers.component.ts

import { JsonPipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-other-household-members',
  standalone: true,
  imports: [ReactiveFormsModule, JsonPipe],
  templateUrl: './otherhouseholdmembers.component.html',
  styleUrls: ['./otherhouseholdmembers.component.css']
})
export class OtherHouseholdMembersComponent implements OnInit {
  otherHouseholdMembersForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.otherHouseholdMembersForm = this.fb.group({
      members: this.fb.array([])
    });
  }

  ngOnInit(): void {
    // Initialize with one member
    this.addMember();
  }

  get members(): FormArray {
    return this.otherHouseholdMembersForm.get('members') as FormArray;
  }

  addMember(): void {
    const memberForm = this.fb.group({
      name: ['', Validators.required],
      age: ['', [Validators.required, Validators.min(0)]],
      relationship: ['', Validators.required]
    });
    this.members.push(memberForm);
  }

  removeMember(index: number): void {
    this.members.removeAt(index);
  }

  onSubmit(): void {
    if (this.otherHouseholdMembersForm.valid) {
      console.log('Form Submitted!', this.otherHouseholdMembersForm.value);
      // Handle form submission logic here
    } else {
      console.log('Form is invalid');
    }
  }
}
