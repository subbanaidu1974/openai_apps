
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { ApplicantComponent } from './applicant.component';
import { By } from '@angular/platform-browser';

describe('ApplicantComponent', () => {
  let component: ApplicantComponent;
  let fixture: ComponentFixture<ApplicantComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ApplicantComponent],
      imports: [ReactiveFormsModule],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ApplicantComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the form', () => {
    expect(component.applicantForm).toBeDefined();
    expect(component.applicantForm.controls['name']).toBeDefined();
    expect(component.applicantForm.controls['email']).toBeDefined();
  });

  it('should mark the name field as invalid if empty', () => {
    const nameControl = component.applicantForm.controls['name'];
    nameControl.setValue('');
    expect(nameControl.valid).toBeFalsy();
  });

  it('should mark the email field as invalid if empty', () => {
    const emailControl = component.applicantForm.controls['email'];
    emailControl.setValue('');
    expect(emailControl.valid).toBeFalsy();
  });

  it('should submit the form when valid', () => {
    const nameControl = component.applicantForm.controls['name'];
    const emailControl = component.applicantForm.controls['email'];

    nameControl.setValue('John Doe');
    emailControl.setValue('john.doe@example.com');

    expect(component.applicantForm.valid).toBeTruthy();

    spyOn(component, 'onSubmit');
    const submitButton = fixture.debugElement.query(By.css('button[type="submit"]'));
    submitButton.nativeElement.click();

    expect(component.onSubmit).toHaveBeenCalled();
  });

  it('should not submit the form when invalid', () => {
    const nameControl = component.applicantForm.controls['name'];
    nameControl.setValue('');

    expect(component.applicantForm.valid).toBeFalsy();

    spyOn(component, 'onSubmit');
    const submitButton = fixture.debugElement.query(By.css('button[type="submit"]'));
    submitButton.nativeElement.click();

    expect(component.onSubmit).not.toHaveBeenCalled();
  });
});
