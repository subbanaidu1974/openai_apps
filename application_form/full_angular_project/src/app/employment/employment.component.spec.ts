
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { EmploymentComponent } from './employment.component';
import { By } from '@angular/platform-browser';

describe('EmploymentComponent', () => {
  let component: EmploymentComponent;
  let fixture: ComponentFixture<EmploymentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EmploymentComponent],
      imports: [ReactiveFormsModule],
      providers: [FormBuilder]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EmploymentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the form', () => {
    expect(component.employmentForm).toBeDefined();
    expect(component.employmentForm.controls['jobTitle']).toBeDefined();
    expect(component.employmentForm.controls['companyName']).toBeDefined();
    expect(component.employmentForm.controls['startDate']).toBeDefined();
    expect(component.employmentForm.controls['endDate']).toBeDefined();
  });

  it('should validate the form fields', () => {
    const jobTitleControl = component.employmentForm.controls['jobTitle'];
    const companyNameControl = component.employmentForm.controls['companyName'];

    // Initially, the form should be invalid
    expect(component.employmentForm.valid).toBeFalsy();

    // Set job title and company name to valid values
    jobTitleControl.setValue('Software Engineer');
    companyNameControl.setValue('Tech Company');

    // Now the form should be valid
    expect(component.employmentForm.valid).toBeTruthy();
  });

  it('should submit the form', () => {
    spyOn(component, 'onSubmit');

    const jobTitleControl = component.employmentForm.controls['jobTitle'];
    const companyNameControl = component.employmentForm.controls['companyName'];

    jobTitleControl.setValue('Software Engineer');
    companyNameControl.setValue('Tech Company');

    const formElement = fixture.debugElement.query(By.css('form'));
    formElement.triggerEventHandler('ngSubmit', null);

    expect(component.onSubmit).toHaveBeenCalled();
  });

  it('should display error messages for invalid fields', () => {
    const jobTitleControl = component.employmentForm.controls['jobTitle'];
    jobTitleControl.setValue('');

    fixture.detectChanges();

    const errorMessage = fixture.debugElement.query(By.css('.job-title-error'));
    expect(errorMessage.nativeElement.textContent).toContain('Job title is required');
  });
});

