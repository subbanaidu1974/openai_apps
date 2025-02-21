import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { SpouseCoApplicantComponent } from './spousecoapplicant.component';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

describe('SpouseCoApplicantComponent', () => {
  let component: SpouseCoApplicantComponent;
  let fixture: ComponentFixture<SpouseCoApplicantComponent>;
  let debugElement: DebugElement;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SpouseCoApplicantComponent],
      imports: [ReactiveFormsModule],
      providers: [FormBuilder]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpouseCoApplicantComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the form', () => {
    expect(component.form).toBeDefined();
    expect(component.form.controls['firstName']).toBeDefined();
    expect(component.form.controls['lastName']).toBeDefined();
    expect(component.form.controls['email']).toBeDefined();
  });

  it('should make the firstName control required', () => {
    const firstNameControl = component.form.get('firstName');
    firstNameControl.setValue('');
    expect(firstNameControl.valid).toBeFalsy();
  });

  it('should submit the form', () => {
    component.form.controls['firstName'].setValue('John');
    component.form.controls['lastName'].setValue('Doe');
    component.form.controls['email'].setValue('john.doe@example.com');

    expect(component.form.valid).toBeTruthy();
    
    spyOn(component, 'onSubmit');
    const submitButton = debugElement.query(By.css('button[type="submit"]'));
    submitButton.nativeElement.click();

    expect(component.onSubmit).toHaveBeenCalled();
  });

  it('should display validation errors', () => {
    const firstNameControl = component.form.get('firstName');
    firstNameControl.setValue('');
    fixture.detectChanges();

    const errorMessage = debugElement.query(By.css('.error-message'));
    expect(errorMessage.nativeElement.textContent).toContain('First Name is required');
  });
});
